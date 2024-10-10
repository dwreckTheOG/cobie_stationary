from flask import render_template, redirect, url_for, abort
from flask_login import current_user, login_required
from app.base import base_bp

# Home route (everyone can access)
@base_bp.route('/')
def index():
    return render_template('index.html')

# Admin dashboard (only accessible to admins)
@base_bp.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'Admin':
        return abort(403)  # Return forbidden if the user is not an Admin
    return render_template('admin_dashboard.html')

# Salesperson dashboard (only accessible to salespersons)
@base_bp.route('/salesperson/dashboard')
@login_required
def salesperson_dashboard():
    if current_user.role != 'Salesperson':
        return abort(403)  # Return forbidden if the user is not a Salesperson
    return render_template('salesperson_dashboard.html')
