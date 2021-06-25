import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure database
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
db = SQLAlchemy(app)

from trader import settings
from trader import models
from trader import routes
