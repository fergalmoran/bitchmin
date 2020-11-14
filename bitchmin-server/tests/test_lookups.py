def test_zones_exist(resolver) -> None:
    answer = resolver.resolve('host-1.bitchmints.com')

    assert answer.address == '10.1.1.1'
