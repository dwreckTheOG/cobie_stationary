from flask import Flask
from config import Config
from app.models import *
from app.extensions import db,login_manager,migrate,b64encode
from datetime import timedelta
from flask import session



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['REMEMBER_COOKIE_DURATION'] = timedelta(minutes=1)

    # Initialize the database
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app,db)
    app.jinja_env.filters['b64encode'] = b64encode
    # Define a custom Jinja2 filter for currency formatting
    def format_currency(value):
        """Format the value as currency."""
        return f"Ksh. {value:,.2f}"

    # Register the filter with Jinja2
    app.jinja_env.filters['currency'] = format_currency

    @login_manager.user_loader
    def load_user(user_id):
        # Extract user type from the session
        user_type = session.get('user_type')

        if user_type == 'customer':
            return Customer.query.get(int(user_id))
        elif user_type == 'user':
            return User.query.get(int(user_id))
        return None



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

    from app.order import order_bp
    app.register_blueprint(order_bp, url_prefix='/order')

    from app.report import report_bp
    app.register_blueprint(report_bp, url_prefix='/report')

    from app.customer import customer_bp
    app.register_blueprint(customer_bp,url_prefix='/customer')

    return app
