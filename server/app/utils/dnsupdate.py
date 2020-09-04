import argparse
import subprocess
import logging

logger = logging.getLogger(__name__)
VERBOSE = True


def __execute_command(command):
    try:
        logger.debug(command)
        result = subprocess.check_output(command, shell=True)

        logger.debug(result)
        return result
    except subprocess.CalledProcessError as e:
        logger.error('Error calling nsupdate command\n{}'.format(e))

    return ''


def update_dns(server, zone, keyfile, domain, ipv4=None, ipv6=None, TTL=30):
    command = "server %s\n" % server
    command += "zone %s\n" % zone
    command += "update delete %s A\n" % domain
    command += "update delete %s AAAA\n" % domain
    if ipv4:
        command += "update add %s %s A %s\n" % (domain, TTL, ipv4)
    if ipv6:
        command += "update add %s %s AAAA %s\n" % (domain, TTL, ipv6)
    command += "show\nsend\n"
    command = "nsupdate -k {0} -v << EOF\n{1}\nEOF\n".format(keyfile, command)

    result = __execute_command(command)

    return True


def delete_record(server, zone, keyfile, domain, TTL=30):
    command = "server %s\n" % server
    command += "zone %s\n" % zone
    command += "update delete %s A\n" % domain
    command += "update delete %s AAAA\n" % domain

    command += "show\nsend\n"
    command = "nsupdate -k {0} -v << EOF\n{1}\nEOF\n".format(keyfile, command)

    result = __execute_command(command)

    return True
