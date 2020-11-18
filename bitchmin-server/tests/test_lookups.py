import dns
import dns.zone
from dns.resolver import NoAnswer


def test_axfr(resolver) -> None:
    try:
        q = dns.query.xfr(
            '127.0.0.1',
            'bitchmints.com',
            port=10053
        )
        query = dns.zone.from_xfr(q)

        assert query is not None and len(query.nodes) != 0
    except Exception as e:
        print(e)
        assert False


def test_ns_records(resolver) -> None:
    host_name = 'bitchmints.com'
    query = resolver.resolve(qname=host_name, rdtype=dns.rdatatype.NS)

    for i in range(0, 2):
        assert str(query[i]) == 'ns-{}.bitchmints.com.'.format(i + 1)


def test_mx_records(resolver) -> None:
    host_name = 'bitchmints.com'
    query = resolver.resolve(qname=host_name, rdtype=dns.rdatatype.MX)

    for i in range(0, 10):
        assert str(query[i].exchange) == 'mail-{}.bitchmints.com.'.format(i + 1)
        assert query[i].preference == i + 1


def test_a_records(resolver) -> None:
    for i in range(1, 11):
        host_name = 'host-{}.bitchmints.com'.format(i)
        try:
            query = resolver.resolve(qname=host_name)

            assert len(query) != 0 and \
                   str(query[0]) == '10.1.1.{}'.format(i)

        except NoAnswer as e:
            print('Host: {} does not exist'.format(host_name))
            assert False
