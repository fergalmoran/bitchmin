import ipaddress
import re
import requests
import sys


def is_valid_ip(address):
    try:
        ip = ipaddress.ip_address(address)
        print('%s is a correct IP%s address.' % (ip, ip.version))
        return True
    except ValueError:
        print('address/netmask is invalid: %s' % sys.argv[1])
    except:
        print('Usage : %s  ip' % sys.argv[0])

    return False


def is_valid_hostname(hostname):
    if len(hostname) > 255:
        return False
    if hostname[-1] == ".":
        hostname = hostname[:-1]  # strip exactly one dot from the right, if present
    allowed = re.compile("(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
    return all(allowed.match(x) for x in hostname.split("."))


def get_my_external_ip():
    ip = requests.get('http://ipinfo.io/json').json()['ip']
    return ip
