from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional

class CustomerForm(FlaskForm):
    customer_name = StringField('Customer Name', validators=[DataRequired(), Length(max=255)])
    email = StringField('Email', validators=[Optional(), Email(), Length(max=255)])
    phone = StringField('Phone', validators=[Optional(), Length(max=20)])
    address = TextAreaField('Address', validators=[Optional()])
    submit = SubmitField('Submit')

class SupplierForm(FlaskForm):
    supplier_name = StringField('Supplier Name', validators=[DataRequired(), Length(max=255)])
    contact_name = StringField('Contact Name', validators=[Optional(), Length(max=255)])
    contact_email = StringField('Contact Email', validators=[Optional(), Email(), Length(max=255)])
    contact_phone = StringField('Contact Phone', validators=[Optional(), Length(max=20)])
    address = TextAreaField('Address', validators=[Optional()])
    submit = SubmitField('Submit')


class UpdateUserForm(FlaskForm):
    full_name = StringField('Full Name', validators=[Optional(), Length(max=255)])
    email = StringField('Email', validators=[Optional(), Email(), Length(max=255)])
    password = PasswordField('Password', validators=[Optional(), Length(min=6)])
    role = SelectField('Role', choices=[('Admin', 'Admin'), ('Salesperson', 'Salesperson')], default='Salesperson')
    submit = SubmitField('Update User')

class UserRegistrationForm(FlaskForm):
    full_name = StringField('Full Name', validators=[Length(max=255)])
    email = StringField('Email', validators=[Email(), Length(max=255)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    role = SelectField('Role', choices=[('Admin', 'Admin'), ('Salesperson', 'Salesperson')], default='Salesperson')
    
    submit = SubmitField('Register')
