from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

from trader.settings import Config
from trader.utils import usd


db = SQLAlchemy()

migrate = Migrate()

login_manager = LoginManager()
login_manager.login_view = "users.login"
login_manager.login_message_category = "info"


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    app.jinja_env.filters["usd"] = usd

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from trader.errors.handlers import errors
    from trader.main.routes import main
    from trader.stocks.routes import stocks
    from trader.users.routes import users

    app.register_blueprint(errors)
    app.register_blueprint(main)
    app.register_blueprint(stocks)
    app.register_blueprint(users)

    return app
