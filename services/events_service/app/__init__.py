from flask import Flask # type: ignore
from .config import Config
from .utils.db import db
from app.routes.event_routes import event_blueprint


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    
    app.register_blueprint(event_blueprint)

    with app.app_context():
        # create database tables if they don't exist
        db.create_all()

    return app

