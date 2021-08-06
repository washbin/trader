#!/usr/bin/env sh

export FLASK_APP=run.py
export FLASK_ENV=development
flask db upgrade
python run.py
