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
