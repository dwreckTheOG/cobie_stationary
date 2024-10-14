from app.auth import auth_bp
from flask import render_template, flash, redirect, url_for, request
from app.auth.forms import LoginForm
from app.models import User  # Assuming User is in models.py
from flask_login import login_user, logout_user # Import login_user if you're using Flask-Login
from werkzeug.security import check_password_hash
from flask import session

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            # Log in the user (assuming you're using Flask-Login)
            session['user_type'] = 'user'
            login_user(user)  # user is an instance of User

            flash('Login successful!', 'success')
            return redirect(url_for('base.index'))  # Redirect to a protected route
        else:
            flash('Login unsuccessful. Please check your email and password.', 'danger')

    return render_template('login.html', form=form)

@auth_bp.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login')) 