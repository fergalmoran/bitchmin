from ipaddress import ip_address

from flask_mail import Message
import os

from sqlalchemy.orm.exc import NoResultFound

from app import create_celery_app, mail, db
from app.models import DnsUpdate, BindState, dnsupdate
import logging
from app.utils import dnsupdate, iputils
from app.utils.twilio import send_sms

logger = logging.getLogger(__name__)
celery = create_celery_app()


@celery.task
def check_host_records():
    platform_ip = iputils.get_my_external_ip()
    logger.debug('Current platform ip: {}'.format(platform_ip))

    try:
        logger.info('Checking for existing state')
        bind_state = BindState.query.one()
    except NoResultFound:
        bind_state = BindState(
            nameserver_1_ip=platform_ip,
            nameserver_1_host=os.getenv('DNSro_SERVER')
        )
        db.session.add(bind_state)
        db.session.commit()

    previous_ip = bind_state.nameserver_1_ip
    if ip_address(platform_ip) != previous_ip:
        logger.info('External IP has changed')
        bind_state.nameserver_1_ip = platform_ip

        logger.info('Updating nameserver record')
        dnsupdate.update_dns(
            os.getenv('DNS_SERVER'),
            os.getenv('DNS_ZONE'),
            os.getenv('DNS_KEY'),
            bind_state.nameserver_1_host,
            platform_ip
        )

        logger.info('Checking host records')
        hosts = DnsUpdate.query.filter_by(ip=previous_ip)
        result = 'Here are the hosts we have\n'
        for host in hosts:
            result += '\tHost: {} IP: {} Date Updated: {}'.format(
                host.host,
                host.ip,
                host.updated_on
            )
            dnsupdate.update_dns(
                os.getenv('DNS_SERVER'),
                os.getenv('DNS_ZONE'),
                os.getenv('DNS_KEY'),
                host.host,
                platform_ip
            )
            host.ip = platform_ip

        logger.info('Saving host details')
        db.session.commit()

        result = 'End of hosts'
        logger.debug(result)
        logger.info('Sending mail')
        try:
            send_sms(
                os.getenv('SMS_NOTIFY_TO'),
                os.getenv('SMS_NOTIFY_FROM'),
                'IP address for {} changed from {} to {}'.format(
                    bind_state.nameserver_1_host,
                    previous_ip,
                    platform_ip
                )
            )

            logger.info('Mail sent successfully')
        except Exception as e:
            logger.error('Unable to send mail report')
            logger.error(e)
    else:
        logger.info('No IP changes detected')
