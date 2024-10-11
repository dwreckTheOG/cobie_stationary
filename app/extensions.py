from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from functools import wraps
from flask_login import current_user
from flask import flash,redirect,url_for

login_manager = LoginManager()

db = SQLAlchemy()



# Utility to check for admin role
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.role != 'Admin':  # Check if the user is not an admin
            flash('You do not have the required permissions.', 'danger')
            return redirect(url_for('reg.view_supplier'))
        return f(*args, **kwargs)
    return decorated_function