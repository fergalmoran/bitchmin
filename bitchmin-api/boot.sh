#!/bin/sh

echo "DB URI ${DATABASE_URL}"
flask db upgrade
exec gunicorn -b :5000 --access-logfile - --error-logfile - server:app
