from flask import Flask
from config import Config
from app.models import *
from app.extensions import db
from flask_migrate import Migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    from app.base import base_bp
    app.register_blueprint(base_bp, url_prefix='')
    return app
