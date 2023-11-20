#!/usr/bin/env bash
if [ -n "$$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$$DJANGO_SUPERUSER_PASSWORD" ] ; then
    (cd ${APP_NAME}; python manage.py createsuperuser --no-input)
fi
(cd app && ./manage.py collectstatic --no-input && gunicorn ${APP_NAME}.wsgi --user www-data --bind 127.0.0.1:${APPLICATION_PORT} --workers 3) &
nginx -g "daemon off;"
