from twilio.rest import Client
import os
import logging

logger = logging.getLogger(__name__)


def send_sms(number_to, number_from, message):
    client = Client(os.getenv('TWILIO_ACCOUNT_SID'), os.getenv('TWILIO_AUTH_TOKEN'))
    logger.debug('Sending SMS')
    message = client.messages.create(
        to=number_to,
        from_=number_from,
        body=message
    )
    logger.debug(message)
