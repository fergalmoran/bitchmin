from app import create_app
from seeder import DbSeeder

if __name__ == '__main__':
    app = create_app()
    ctx = app.app_context()
    ctx.push()
    from app import db

    db.app = app

    DbSeeder(db).seed()
