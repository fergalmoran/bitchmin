from flask_migrate import Migrate, upgrade
from app import create_app, db, create_celery_app

app = create_app()
celery = create_celery_app()

migrate = Migrate(app, db)


@app.cli.command()
def deploy():
    """Run deployment tasks"""
    # Migrate database to latest revision
    upgrade()
