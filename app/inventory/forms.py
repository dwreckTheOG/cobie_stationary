from flask_wtf import FlaskForm
from wtforms import HiddenField,TextAreaField, DateTimeField,StringField, DecimalField, IntegerField, BooleanField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Length
from wtforms.fields import DateTimeLocalField
from datetime import datetime

class InventoryForm(FlaskForm):
    product_id = HiddenField('Product', validators=[DataRequired()])  # Hidden field for product_id
    stock_in = IntegerField('Stock In', validators=[DataRequired(), NumberRange(min=0)])
    stock_out = IntegerField('Stock Out', validators=[DataRequired(), NumberRange(min=0)])
    date = DateTimeLocalField('Date', format='%Y-%m-%dT%H:%M', default=datetime.now)
    submit = SubmitField('Update Inventory')

class ProductForm(FlaskForm):
    product_name = StringField('Product Name', validators=[DataRequired()])
    product_code = StringField('Product Code', validators=[DataRequired()])  # New field for product code
    category_id = SelectField('Category', choices=[], coerce=int, validators=[DataRequired()])
    supplier_id = SelectField('Supplier', choices=[], coerce=int, validators=[DataRequired()])
    unit_price = DecimalField('Unit Price', validators=[DataRequired()])
    stock_quantity = IntegerField('Stock Quantity', validators=[DataRequired()])
    reorder_level = IntegerField('Reorder Level', validators=[DataRequired()])
    discontinued = BooleanField('Discontinued')
    
class CategoryForm(FlaskForm):
    category_name = StringField(
        'Category Name', 
        validators=[DataRequired(), Length(max=255)]
    )
    description = TextAreaField(
        'Description', 
        validators=[Length(max=500)]
    )
    submit = SubmitField('Save Category')
