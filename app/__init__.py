from flask import Flask
from config import Config
from app.models import *
from app.extensions import db,login_manager,migrate
from datetime import timedelta


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['REMEMBER_COOKIE_DURATION'] = timedelta(minutes=1)

    # Initialize the database
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    migrate.init_app(app,db)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


    with app.app_context():
        db.create_all()  # Creates tables if they don't exist

    # Register blueprints
    from app.base import base_bp
    app.register_blueprint(base_bp, url_prefix='')

    from app.reg import reg_bp
    app.register_blueprint(reg_bp, url_prefix='/reg')

    from app.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.inventory import inventory_bp
    app.register_blueprint(inventory_bp, url_prefix='/inventory')

    return app
