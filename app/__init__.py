from flask import Flask
from config import Config
from app.models import *
from app.extensions import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize the database
    db.init_app(app)

    with app.app_context():
        db.create_all()  # Creates tables if they don't exist

    # Register blueprints
    from app.base import base_bp
    app.register_blueprint(base_bp, url_prefix='')

    from app.reg import reg_bp
    app.register_blueprint(reg_bp, url_prefix='/reg')

    from app.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app
