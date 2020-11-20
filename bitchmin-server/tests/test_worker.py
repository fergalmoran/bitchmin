import dns
import dns.zone
from dns.resolver import NoAnswer


def test_add_record(resolver) -> None:
    assert False