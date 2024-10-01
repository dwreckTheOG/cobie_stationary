import base64
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_login import LoginManager

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    return app
