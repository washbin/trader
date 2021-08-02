#!/usr/bin/env sh

export FLASK_APP=run.py
flask db upgrade
gunicorn -b 0.0.0.0:5000 run:app
