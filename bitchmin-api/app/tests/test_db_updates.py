import uuid

import pytest
from sqlalchemy import func

from app.models import User, DnsZone, DnsNameServer, DnsHost
from scaffolder import Scaffolder


@pytest.fixture(scope="function")  # or "module" (to teardown at a module level)
def db():
    scaffolder = Scaffolder()
    scaffolder.teardown()
    scaffolder.scaffold()

    yield scaffolder.session

    scaffolder.teardown()


class TestDatabaseUpdate:
    def test_load(self, db) -> None:
        assert db.query(User).count() == 1
        assert db.query(DnsZone).count() == 1
        assert db.query(DnsNameServer).count() == 2
        assert db.query(DnsHost).count() == 10

    def test_serial_on_create(self, db) -> None:
        zone = db.query(DnsZone).first()
        assert len(str(zone.serial)) == 10
        assert zone.get_serial_increment() == 10

    def test_serial_on_add_host(self, db) -> None:
        zone = db.query(DnsZone).first()
        serial = zone.get_serial_increment()

        DnsHost(
            zone=zone,
            host=str(uuid.uuid4()),
            ip='99.99.99.99'
        )
        db.commit()
        """
            Probably better to test that the new serial is > old serial... 
            Not hugely important that it's only ONE more than it
        """
        assert zone.get_serial_increment() > serial

    def test_serial_on_update_host(self, db) -> None:
        host = db.query(DnsHost).get(4)
        serial = host.zone.get_serial_increment()

        host.ip = '99.99.99.99'
        db.commit()

        assert host.zone.get_serial_increment() > serial

