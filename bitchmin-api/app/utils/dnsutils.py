import pydig


def get_dns_records(host, ip, server):
    resolver = pydig.Resolver(
        nameservers=[
            server
        ]
    )
    result = resolver.query(host, 'A')

    return result

