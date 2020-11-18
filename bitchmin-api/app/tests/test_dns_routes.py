import json


class TestUserRoutes:

    def test_get_hosts(self, db, app) -> None:
        client = app.test_client()
        rv = client.get(f"/dns/zones")
        assert "200" in rv.status
        zones = json.loads(rv.data)
        assert len(zones) == 1
        assert zones[0]['name'] == 'bitchmints.com'
        assert len(zones[0]['nameservers']) == 2
        assert zones[0]['nameservers'][0]['name'] == 'host-1.bitchmints.com'
        assert zones[0]['nameservers'][1]['name'] == 'host-2.bitchmints.com'
        assert zones[0]['nameservers'][0]['ip'] == '10.1.1.101'
        assert zones[0]['nameservers'][1]['ip'] == '10.1.1.102'
