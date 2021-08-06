#!/usr/bin/env sh

export FLASK_APP=run.py
export FLASK_ENV=production
flask db upgrade
gunicorn --bind 0.0.0.0:5000 run:app
