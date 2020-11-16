import pytest

from app import create_app
from app import db as _db
from .seeder import DbSeeder


@pytest.fixture()
def app(request):
    app = create_app()
    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return app


@pytest.fixture()
def db(app, request):
    _db.app = app
    seeder = DbSeeder(_db)
    seeder.seed()

    def teardown():
        seeder.teardown()

    request.addfinalizer(teardown)

    return _db
