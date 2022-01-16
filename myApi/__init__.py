from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from myApi.config import Config

db = SQLAlchemy()
app_session = Session()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    app_session.init_app(app)

    from myApi.users.routes import users

    app.register_blueprint(users)

    return app
