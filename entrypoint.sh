#!/usr/bin/env sh

export FLASK_APP=run.py
flask db upgrade
python run.py
