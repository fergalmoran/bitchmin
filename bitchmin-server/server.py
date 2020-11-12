import logging

from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.names import client, dns, server

from resolvers.memory_resolver import MemoryResolver
from servers.worker_server import WorkerServerFactory

logging.basicConfig(level=logging.DEBUG)

PORT = 10053
WORKER_PORT = 10054


def main():
    zones = {
        'bitchmints.com': {
            'serial': 'BOOO',
            'admin': 'Ferg@lMoran.me',
            'nameservers': [
                'ns1.bitchmints.com',
                'ns2.bitchmints.com'
            ],
            'hosts': {
                'ns1': {'type': 'A', 'ttl': 30, 'ip': '10.1.33.7'},
                'ns2': {'type': 'A', 'ttl': 30, 'ip': '10.1.33.8'},
                'host-1': {'type': 'A', 'ttl': 30, 'ip': '10.1.33.1'},
                'host-2': {'type': 'A', 'ttl': 30, 'ip': '10.1.33.1'},
                'host-3': {'type': 'A', 'ttl': 30, 'ip': '10.1.33.1'},
                'host-4': {'type': 'A', 'ttl': 30, 'ip': '10.1.33.1'},
            }
        },
        'fergl.ie': {
            'serial': 'BOOO',
            'admin': 'Ferg@lMoran.me',
            'nameservers': [
                'ns1.bitchmints.com',
                'ns2.bitchmints.com'
            ],
            'hosts': {
                'farts': {'type': 'A', 'ttl': 30, 'ip': '10.1.33.8'},
            }
        }
    }

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
