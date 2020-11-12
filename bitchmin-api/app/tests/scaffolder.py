import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app import db
from app.models import DnsZone, User, DnsHost, DnsNameServer


class Scaffolder(object):
    engine = create_engine(
        'postgresql+psycopg2://bitchmin:bitchmin@localhost/bitchmin',
        poolclass=StaticPool)
    Session = sessionmaker(bind=engine)
    session = Session()

    def _create_user(self):
        user = User(
            'fergal.moran@gmail.com',
            'Fergal Moran',
            'topsecret'
        )
        self.session.add(user)

    def _create_zone(self):
        zone = DnsZone('bitchmints.com')
        self.session.add(zone)
        return zone

    def _create_nameservers(self, zone):
        for i in range(1, 3):
            ns = DnsNameServer(
                zone,
                'host-{}'.format(i),
                '10.1.1.10{}'.format(i)

            )
            self.session.add(ns)

    def _create_hosts(self, zone):
        for i in range(1, 11):
            host = DnsHost(
                zone,
                'host-{}'.format(i),
                '10.1.1.{}'.format(i)
            )
            self.session.add(host)

    def scaffold(self):
        db.metadata.drop_all(self.engine)
        db.metadata.create_all(self.engine)

        self._create_user()
        z = self._create_zone()
        self._create_nameservers(z)
        self._create_hosts(z)

        self.session.commit()
        self.session.flush()

    def teardown(self):
        db.metadata.drop_all(self.engine)
        self.engine.dispose()


if __name__ == '__main__':
    Scaffolder().scaffold()
