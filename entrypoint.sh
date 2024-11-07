#!/bin/sh

if [ "$APP_ENV" = "production" ]; then
    exec gunicorn --bind 0.0.0.0:5000 app:app
else
    exec python app.py
fi