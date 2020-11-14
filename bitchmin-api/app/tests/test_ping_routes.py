from datetime import timedelta

from app.models import User


class TestUserRoutes:

    def test_user_get(self, db, app) -> None:
        client = app.test_client()
        rv = client.get(f"/ping")
        assert "200" in rv.status
        assert "pong!" in str(rv.data)
