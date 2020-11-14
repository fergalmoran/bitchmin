from datetime import timedelta

from app.models import User


class TestAuthRoutes:
    def test_no_duplicate_registration(self, db, app) -> None:
        client = app.test_client()

        request = {
            'email': 'fergal.moran@gmail.com',
            'full_name': 'Fergal Moran',
            'password': 'topsecret'
        }

        rv = client.post(f"/auth/register/", json=request)
        assert "409" in rv.status

    def test_registration(self, db, app) -> None:
        client = app.test_client()

        request = {
            'email': 'fergal.moran+testuser@gmail.com',
            'full_name': 'Fergal Moran Test User',
            'password': 'topsecret2'
        }

        rv = client.post(f"/auth/register/", json=request)
        assert "201" in rv.status

    def test_login_fails(self, db, app) -> None:
        client = app.test_client()

        request = {
            'email': 'fergal.moran@gmail.com',
            'password': 'asdasda'
        }

        rv = client.post(f"/auth/login/", json=request)
        assert "401" in rv.status

    def test_login_succeeds(self, db, app) -> None:
        client = app.test_client()

        request = {
            'email': 'fergal.moran@gmail.com',
            'password': 'topsecret'
        }

        rv = client.post(f"/auth/login/", json=request)
        assert "200" in rv.status
