from twisted.internet import defer
from twisted.names import dns, error
import logging


class InvalidZoneException(Exception):
    pass


class Resolver:
    def _build_host(self, record_type, host, ip, ttl):
        return {
            host: {
                'type': record_type,
                'ttl': ttl,
                'ip': ip
            },
        }


class MemoryResolver(Resolver):
    """
    A resolver which calculates the answers to certain queries based on the
    query type and name.
    """

    def __init__(self, zones):
        self._zones = zones

    def add_host(self, record_type, zone, host, ip, ttl):
        if self._zones[zone]:
            # 'ns1': {'type': 'A', 'ttl': 30, 'ip': '10.1.33.7'},
            new = {
                host: {
                    'type': record_type,
                    'ttl': ttl,
                    'ip': ip
                },
            }
            try:
                self._zones[zone]['hosts'].update(new)
            except Exception as e:
                logging.error(e)
        else:
            raise InvalidZoneException('Zone {} does not exist'.format(zone))

    @staticmethod
    def _parse_host(zone, host):
        parsed = [x for x in host.split('.') if x not in zone.split('.')]
        return '.'.join(parsed) if len(parsed) != 0 else ''

    def _get_authoritative_zone(self, query):
        """
        split on "." and keep removing from left until we find a zone or we run out of string
        """
        parts = str(query.name).split('.')
        while len(parts) != 0:
            t = '.'.join(parts)
            if t in self._zones:
                return t, self._zones[t]
            parts.pop(0)

        return None

    def _get_response(self, zone, query):
        """
        Calculate the response to a query.
        """
        try:
            host = self._parse_host(zone, str(query.name))
            record = self._zones[zone]['hosts'][host]

            if query.type == dns.NS:
                payload = dns.Record_NS(
                    name=zone['nameservers'][0],
                    ttl=record['ttl']
                )
            else:
                payload = dns.Record_A(
                    address=record['ip'],
                    ttl=record['ttl']
                )

            answer = dns.RRHeader(
                name=zone,
                payload=payload,
                ttl=record['ttl']
            )

            answers = [answer]
            authority = []
            additional = []

            return answers, authority, additional

        except KeyError:
            return None

    def query(self, query, timeout=None):
        """
        Check if the query should be answered dynamically, otherwise dispatch to
        the fallback resolver.
        """

        logging.info(query)
        name, zone = self._get_authoritative_zone(query)
        if zone and name:
            logging.debug('BitchNS: Authoritative for {}'.format(name))
            result = self._get_response(name, query)
            if result:
                logging.debug('BitchNS: Resolving {} to {}'.format(name, result))
                return defer.succeed(result)
            logging.debug('BitchNS: Host {} not found in zone {}'.format(name, zone))

        return defer.fail(error.DomainError())
