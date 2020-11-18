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

        for i in range(0, 2):
            assert zones[0]['nameservers'][i]['ip'] == '10.1.1.10{}'.format(i + 1)
            assert zones[0]['nameservers'][i]['name'] == 'host-{}.bitchmints.com'.format(i + 1)

        for i in range(0, 10):
            assert zones[0]['mailexchangers'][i]['name'] == 'mail-{}.bitchmints.com'.format(i + 1)
            assert zones[0]['mailexchangers'][i]['preference'] == i + 1
