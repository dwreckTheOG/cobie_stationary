from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from functools import wraps
from flask import flash, redirect, url_for
from flask_migrate import Migrate
import base64

def b64encode(data):
    if data:
        return base64.b64encode(data).decode('utf-8')
    return None


login_manager = LoginManager()
db = SQLAlchemy()
migrate = Migrate()

# Utility to check for admin role
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if the user is authenticated
        if not current_user.is_authenticated:
            flash('You need to be logged in to access this page.', 'danger')
            return redirect(url_for('auth.login'))  # Adjust to your login route

        # Check if the user has the admin role
        if current_user.role != 'Admin':
            flash('You do not have the required permissions.', 'danger')
            return redirect(url_for('base.index'))  # Adjust to your desired redirect route
        
        return f(*args, **kwargs)
    return decorated_function
