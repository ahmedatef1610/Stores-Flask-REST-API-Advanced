#!/bin/sh

flask db upgrade

# exec gunicorn --bind 0.0.0.0:80 "app:create_app()"

# exec gunicorn --bind 0.0.0.0:8080 "app:app"

exec gunicorn --bind 0.0.0.0:8080 "app:create_app()"

