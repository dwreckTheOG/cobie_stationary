from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class UserRegistrationForm(FlaskForm):
    full_name = StringField('Full Name', validators=[Length(max=255)])
    email = StringField('Email', validators=[Email(), Length(max=255)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    role = SelectField('Role', choices=[('Admin', 'Admin'), ('Salesperson', 'Salesperson')], default='Salesperson')
    
    submit = SubmitField('Register')
