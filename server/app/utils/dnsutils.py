import pydig


def validate_dns_record(host, ip, server):
    resolver = pydig.Resolver(
        nameservers=[
            server
        ]
    )
    result = resolver.query(host, 'A')
    print('Result is: {}\nSuccess: {}'.format(result, ip in result))

    return ip in result
