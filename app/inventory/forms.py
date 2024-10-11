from flask_wtf import FlaskForm
from wtforms import TextAreaField, DateTimeField,StringField, DecimalField, IntegerField, BooleanField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Length

class InventoryForm(FlaskForm):
    product_id = SelectField('Product', coerce=int)  # This will need a query to populate choices
    stock_in = IntegerField('Stock In', validators=[DataRequired(), NumberRange(min=0)])
    stock_out = IntegerField('Stock Out', validators=[DataRequired(), NumberRange(min=0)])
    date = DateTimeField('Date', format='%Y-%m-%d %H:%M:%S', validators=[DataRequired()])
    submit = SubmitField('Update Inventory')

class ProductForm(FlaskForm):
    product_name = StringField('Product Name', validators=[DataRequired()])
    category_id = SelectField('Category', coerce=int)  # This will need a query to populate choices
    supplier_id = SelectField('Supplier', coerce=int)  # This will need a query to populate choices
    unit_price = DecimalField('Unit Price', validators=[DataRequired(), NumberRange(min=0)], places=2)
    stock_quantity = IntegerField('Stock Quantity', validators=[DataRequired(), NumberRange(min=0)])
    reorder_level = IntegerField('Reorder Level', validators=[DataRequired(), NumberRange(min=0)])
    discontinued = BooleanField('Discontinued')
    submit = SubmitField('Save Product')

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
