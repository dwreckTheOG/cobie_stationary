from flask import render_template, redirect, url_for, flash
from app.reg import reg_bp
from app.reg.forms import UserRegistrationForm
from app.models import User
from app.extensions import db
from werkzeug.security import generate_password_hash

@reg_bp.route('/user/registration', methods=['GET', 'POST'])
def user_registration():
    form = UserRegistrationForm()

    if form.validate_on_submit():
        # Hash the password
        hashed_password = generate_password_hash(form.password.data)
        
        # Create a new user object
        new_user = User(
            full_name=form.full_name.data,
            email=form.email.data,
            password_hash=hashed_password,
            role=form.role.data
        )
        
        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        # Provide feedback to the user
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('auth.login'))  # Redirect to login page (assuming you have a login route)
    
    # Render the registration template with the form
    return render_template('user_registration.html', form=form)
