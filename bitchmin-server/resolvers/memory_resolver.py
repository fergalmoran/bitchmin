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
            auth=True,
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

        n = next(iter(zone.nameservers))
        record = dns.Record_NS(
            name=zone.nameservers[n].name,
            ttl=zone.nameservers[n].ttl
        )

        authority = [
            dns.RRHeader(
                zone.name,
                type=dns.NS,
                ttl=0xFFFFFFFF,
                auth=True,
                payload=record,
            )
        ]
        records.append(
            dns.RRHeader(
                zone.name,
                type=dns.NS,
                cls=dns.IN,
                ttl=700,
                auth=False,
                payload=record,
            )
        )
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

        return records, authority, ()


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

            host = self._parse_host(zone_name, str(query.name))
            answers = []
            authority = []
            additional = []

            if query.type == dns.AXFR:
                return self._gen_axfr(zone_name)

            if query.type == dns.NS:
                self._get_nameservers(answers, query, zone_name)
            elif query.type == dns.MX:
                self._get_mailexchangers(answers, query, zone_name)
            else:
                record = self._zones[zone_name].hosts[host]
                answers.append(dns.RRHeader(
                    name=str(query.name),
                    payload=dns.Record_A(
                        address=record.ip,
                        ttl=record.ttl
                    ),
                    ttl=record.ttl
                ))

            return answers, authority, additional

        except KeyError:
            return None

    def _get_nameservers(self, answers, query, zone_name):
        for ns in self._zones[zone_name].nameservers:
            answers.append(
                dns.RRHeader(
                    name=str(query.name),
                    type=dns.NS,
                    ttl=self._zones[zone_name].nameservers[ns].ttl,
                    payload=dns.Record_NS(
                        name=self._zones[zone_name].nameservers[ns].name,
                        ttl=self._zones[zone_name].nameservers[ns].ttl
                    )
                )
            )

    def _get_mailexchangers(self, answers, query, zone_name):
        for mx in self._zones[zone_name].mailexchangers:
            answers.append(
                dns.RRHeader(
                    name=str(query.name),
                    type=dns.MX,
                    ttl=self._zones[zone_name].mailexchangers[mx].ttl,
                    payload=dns.Record_MX(
                        name=self._zones[zone_name].mailexchangers[mx].name,
                        ttl=self._zones[zone_name].mailexchangers[mx].ttl,
                        preference=self._zones[zone_name].mailexchangers[mx].preference
                    )
                )
            )

    def query(self, query, timeout=None):
        """
        Check if the query should be answered dynamically, otherwise dispatch to
        the fallback resolver.
        """

        logging.info(query)
        zone_name, zone = self._get_authoritative_zone(query)
        if zone and zone_name:
            logging.debug('BitchNS: Authoritative for {}'.format(zone_name))
            result = self._get_response(zone_name, query)
            if result:
                logging.debug('BitchNS: Resolving {} to {}'.format(zone_name, result))
                return defer.succeed(result)

        logging.error('Query failure')
        return defer.fail(error.DomainError())
