import requests
from twisted.internet import defer
from twisted.names import dns, error
import logging


class InvalidZoneException(Exception):
    pass


class Resolver:
    """
    A resolver which calculates the answers to certain queries based on the
    query type and name.
    """

    def __init__(self, zones):
        self._zones = zones

    @staticmethod
    def _build_host(record_type, host, ip, ttl):
        return {
            host: {
                'type': record_type,
                'ttl': ttl,
                'ip': ip
            },
        }

    def _gen_axfr(self, zone_name):
        zone = self._zones[zone_name]

        records = []
        soa = dns.RRHeader(
            name=zone.name,
            type=dns.SOA,
            cls=dns.IN,
            ttl=86400,
            auth=False,
            payload=dns.Record_SOA(
                mname=next(iter(zone.nameservers)),
                rname='Ferg@lMoran.me',  # TODO: store this
                serial=zone.serial,
                refresh=10,
                retry=10,
                expire=2000,
                minimum=100,
                ttl=100)
        )

        records.append(soa)
        for h in zone.hosts:
            host = zone.hosts[h]
            record = dns.RRHeader(
                '{}.{}'.format(host.name, zone.name),
                dns.A,
                dns.IN,
                host.ttl,
                dns.Record_A(host.ip, host.ttl))
            records.append(record)

        records.append(soa)

        return records, (), ()


class MemoryResolver(Resolver):

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

    def _get_response(self, zone_name, query):
        """
        Calculate the response to a query.
        """
        try:
            # try named domain requests first
            if zone_name not in self._zones:
                return None

            if query.type == dns.AXFR:
                return self._gen_axfr(zone_name)

            host = self._parse_host(zone_name, str(query.name))
            record = self._zones[zone_name].hosts[host]

            if query.type == dns.NS:
                payload = dns.Record_NS(
                    name=zone_name['nameservers'][0],
                    ttl=record['ttl']
                )
            else:
                payload = dns.Record_A(
                    address=record.ip,
                    ttl=record.ttl
                )

            answer = dns.RRHeader(
                name=zone_name,
                payload=payload,
                ttl=record.ttl
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
