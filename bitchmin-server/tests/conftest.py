import pytest


@pytest.fixture()
def resolver():
    import dns.resolver

    r = dns.resolver.Resolver()

    r.nameservers = ['127.0.0.1']
    r.nameserver_ports = {
        '127.0.0.1': 10053
    }
    return r
