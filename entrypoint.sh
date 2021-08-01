#!/usr/bin/env sh

export FLASK_APP=run.py
flask db upgrade
gunicorn --bind 0.0.0.0:5000 run:app
