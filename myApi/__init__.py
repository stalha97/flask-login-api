from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from myApi.config import Config

db = SQLAlchemy()
sess = Session()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    sess.init_app(app)

    from myApi.users.routes import users

    # from flaskblog.posts.routes import posts
    # from flaskblog.main.routes import main

    app.register_blueprint(users)
    # app.register_blueprint(posts)
    # app.register_blueprint(main)

    return app
