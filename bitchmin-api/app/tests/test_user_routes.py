from datetime import timedelta

from app.models import User


class TestUserRoutes:

    def test_user_get(self, db, app) -> None:
        client = app.test_client()
        user = db.session.query(User).first()
        token = user.create_token(timedelta(seconds=60))

        rv = client.get(f"/user", headers={"Authorization": "Bearer {}".format(token)})
        assert "200" in rv.status
