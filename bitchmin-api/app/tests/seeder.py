from app.models import DnsZone, User, DnsHost, DnsNameServer


class DbSeeder(object):

    def __init__(self, database):
        self._db = database

    def _create_user(self):
        user = User(
            'fergal.moran@gmail.com',
            'Fergal Moran',
            'topsecret'
        )
        self._db.session.add(user)

    def _create_zone(self):
        zone = DnsZone('bitchmints.com')
        self._db.session.add(zone)
        return zone

    def _create_nameservers(self, zone):
        for i in range(1, 3):
            ns = DnsNameServer(
                zone,
                'host-{}'.format(i),
                '10.1.1.10{}'.format(i)

            )
            self._db.session.add(ns)

    def _create_hosts(self, zone):
        for i in range(1, 11):
            host = DnsHost(
                zone,
                'host-{}'.format(i),
                '10.1.1.{}'.format(i)
            )
            self._db.session.add(host)

    def seed(self):
        self._db.metadata.drop_all(self._db.engine)
        self._db.metadata.create_all(self._db.engine)

        self._create_user()
        z = self._create_zone()
        self._create_nameservers(z)
        self._create_hosts(z)

        self._db.session.commit()
        self._db.session.flush()

    def teardown(self):
        self._db.metadata.drop_all(self._db.engine)
        self._db.engine.dispose()
