from flask import render_template, redirect, url_for, flash
from app.reg import reg_bp
from app.reg.forms import UserRegistrationForm, UpdateUserForm
from app.models import User
from app.extensions import db
from werkzeug.security import generate_password_hash
from flask_login import login_required

@reg_bp.route('/delete/user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    
    try:
        db.session.delete(user)
        db.session.commit()
        flash('User deleted successfully.', 'success')
    except:
        db.session.rollback()
        flash('An error occurred. User could not be deleted.', 'danger')
    
    return redirect(url_for('reg.view_users'))

@reg_bp.route('/update/user/<int:user_id>', methods=['GET', 'POST'])
@login_required  # Ensure the user is logged in to perform this action
def update_user(user_id):
    user = User.query.get_or_404(user_id)  # Fetch the user by ID
    form = UpdateUserForm(obj=user)  # Prepopulate form with user data

    if form.validate_on_submit():
        # Update user details
        user.full_name = form.full_name.data
        user.email = form.email.data
        user.role = form.role.data

        # Update password if provided
        if form.password.data:
            user.password_hash = generate_password_hash(form.password.data)
        
        db.session.commit()  # Commit the changes to the database
        flash('User updated successfully!', 'success')
        
        return redirect(url_for('reg.view_users'))  # Redirect to view users

    return render_template('update_user.html', form=form, user=user)

@reg_bp.route('/view/users')
@login_required
def view_users():
    users = User.query.all()
    return render_template('view_users.html',users=users)

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
