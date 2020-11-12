class Command:
    pass


class AddRecordCommand(Command):
    def __init__(self, record_type, zone, host, ip, ttl):
        self.type = record_type
        self.zone = zone
        self.host = host
        self.ip = ip
        self.ttl = ttl

    def __str__(self):
        return 'AddRecordCommand({}) - Host: {} IP: {}'.format(
            self.type,
            self.zone,
            self.host,
            self.ip,
        )
