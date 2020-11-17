import json
import logging
import os

import requests
from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.names import client, dns, server

from models.zone import Zone
from resolvers.memory_resolver import MemoryResolver
from servers.worker_server import WorkerServerFactory

logging.basicConfig(level=logging.DEBUG)

PORT = int(os.environ.get('DNS_PORT') or 10053)
WORKER_PORT = int(os.environ.get('WORKER_PORT') or 10054)
API_HOST = os.environ.get('API_HOST') or 'http://localhost:5000'


# TODO: This smells
def get_zones():
    response = requests.get('{}/dns/zones'.format(API_HOST))
    zones = Zone.from_json(response.text)
    return {
        zone.name: zone
        for zone in zones
    }


def main():
    zones = get_zones()
    memory_resolver = MemoryResolver(zones)

    dns_factory = server.DNSServerFactory(
        clients=[
            memory_resolver,
            client.Resolver(resolv='/etc/resolv.conf')]
    )

    protocol = dns.DNSDatagramProtocol(controller=dns_factory)

    logging.info('BitchNS: Starting UDP/ns listener on {}'.format(PORT))
    reactor.listenUDP(PORT, protocol)

    logging.info('BitchNS: Starting TCP/ns listener on {}'.format(PORT))
    reactor.listenTCP(PORT, dns_factory)

    logging.info('BitchNS: Starting TCP/worker listener on {}'.format(WORKER_PORT))
    worker_factory = TCP4ServerEndpoint(reactor, WORKER_PORT)
    worker_factory.listen(WorkerServerFactory(memory_resolver))

    reactor.run()


if __name__ == '__main__':
    logging.debug('BitchNS: Server starting')
    raise SystemExit(main())
