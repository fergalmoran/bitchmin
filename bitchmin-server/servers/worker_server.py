from twisted.internet.protocol import Protocol, Factory

from resolvers.commands import AddRecordCommand
import logging


class WorkerServerFactory(Factory):
    def __init__(self, resolver):
        self._resolver = resolver

    def buildProtocol(self, addr):
        return WorkerServer(self._resolver)


class UnknownCommandException(Exception):
    pass


class WorkerServer(Protocol):
    def __init__(self, resolver):
        self._resolver = resolver

    def dataReceived(self, data):
        logging.debug('BitchNS: Command received: {}'.format(data))
        try:
            command = self.__parse_data(data)
            logging.debug('BitchNS: {}'.format(command))
            self._resolver.add_host(
                record_type=command.type,
                zone=command.zone,
                host=command.host,
                ip=command.ip,
                ttl=command.ttl
            )
            self.__send_response(str(command))

        except UnknownCommandException as e:
            self.__send_response('Unable to parse command: {0}'.format(e))

    def __send_response(self, response):
        self.transport.write(bytes(
            '{}\n'.format(
                response
            ).encode('utf-8')
        ))

    @staticmethod
    def __parse_data(data):
        parts = data.decode('utf-8').split('|')
        if parts[0] == 'A':
            return AddRecordCommand(
                record_type=parts[1],
                zone=parts[2],
                host=parts[3],
                ip=parts[4],
                ttl=parts[5]
            )

        raise UnknownCommandException(data)
