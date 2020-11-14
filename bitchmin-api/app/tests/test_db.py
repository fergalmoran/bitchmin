import uuid

from app.models import User, DnsZone, DnsNameServer, DnsHost


class TestDatabaseUpdate:
    def test_load(self, db) -> None:
        assert db.session.query(User).count() == 1
        assert db.session.query(DnsZone).count() == 1
        assert db.session.query(DnsNameServer).count() == 2
        assert db.session.query(DnsHost).count() == 10

    def test_serial_on_create(self, db) -> None:
        zone = db.session.query(DnsZone).first()
        assert len(str(zone.serial)) == 10
        assert zone.get_serial_increment() == 10

    def test_serial_on_add_host(self, db) -> None:
        zone = db.session.query(DnsZone).first()
        serial = zone.get_serial_increment()

        DnsHost(
            zone=zone,
            host=str(uuid.uuid4()),
            ip='99.99.99.99'
        )
        db.session.commit()
        """
            Probably better to test that the new serial is > old serial... 
            Not hugely important that it's only ONE more than it
        """
        assert zone.get_serial_increment() > serial

    def test_serial_on_update_host(self, db) -> None:
        host = db.session.query(DnsHost).get(4)
        serial = host.zone.get_serial_increment()

        host.ip = '99.99.99.99'
        db.session.commit()

        assert host.zone.get_serial_increment() > serial
