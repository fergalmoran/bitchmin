#!/bin/sh

# Run Celery worker
celery -A app.celery worker --loglevel=DEBUG --detach --pidfile=''

# Run Celery Beat
celery -A app.celery beat --loglevel=DEBUG --detach --pidfile=''

flask run