from flask_wtf import FlaskForm
from wtforms import IntegerField, DateTimeLocalField, DecimalField, SelectField, SubmitField
from wtforms.validators import DataRequired, Optional, NumberRange
from datetime import datetime

class OrderStatusForm(FlaskForm):
    status = SelectField('Status', choices=[
        ('Pending', 'Pending'),
        ('Sorting', 'Sorting'),
        ('Transporting', 'Transporting'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled')
    ], validators=[DataRequired()])
    
    submit = SubmitField('Update Status')

class SaleForm(FlaskForm):
    customer_id = IntegerField('Customer ID', validators=[Optional(), NumberRange(min=1)])
    user_id = IntegerField('User ID', validators=[DataRequired(), NumberRange(min=1)])  # Assuming user_id is required
    sale_date = DateTimeLocalField('Sale Date', format='%Y-%m-%dT%H:%M', default=datetime.now)
    total_amount = DecimalField('Total Amount', places=2, validators=[DataRequired(), NumberRange(min=0)])
    payment_status = SelectField('Payment Status', choices=[
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Cancelled', 'Cancelled')
    ], default='Pending')
    submit = SubmitField('Create Sale')

class SalesItemForm(FlaskForm):
    sale_id = IntegerField('Sale ID', validators=[DataRequired()])
    product_code = SelectField('Product Code', coerce=str, validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1)])
    total_price = DecimalField('Total Price', places=2, validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(SalesItemForm, self).__init__(*args, **kwargs)
        self.product_code.choices = [(p.product_code, p.product_code) for p in Product.query.all()]  # Populate product codes from the database
        
class PaymentForm(FlaskForm):
    sale_id = IntegerField('Sale ID', validators=[DataRequired(), NumberRange(min=1)])
    order_id = IntegerField('Order ID', validators=[DataRequired(), NumberRange(min=1)])  # Add order_id field
    amount_paid = DecimalField('Amount Paid', places=2, validators=[DataRequired(), NumberRange(min=0)])
    payment_method = SelectField('Payment Method', 
                                  choices=[('Cash', 'Cash'), 
                                           ('M-Pesa', 'M-Pesa')],  # Updated choices
                                  validators=[DataRequired()])
    payment_date = DateTimeLocalField('Payment Date', 
                                       format='%Y-%m-%dT%H:%M',
                                       default=datetime.now,
                                       validators=[DataRequired()])
    submit = SubmitField('Add Payment')