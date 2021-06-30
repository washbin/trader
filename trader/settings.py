import os
from tempfile import mkdtemp


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    # Ensure templates are auto-reloaded
    TEMPLATES_AUTO_RELOAD = True
    # Configure session to use filesystem (instead of signed cookies)
    SESSION_FILE_DIR = mkdtemp()
    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"
    # disabling cache
    SEND_FILE_MAX_AGE_DEFAULT = 0
