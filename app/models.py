from app.extensions import db
from flask_login import UserMixin

class Category(db.Model):
    __tablename__ = 'categories'
    
    category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)

    # Relationships
    products = db.relationship('Product', backref='category', lazy=True)

    def __repr__(self):
        return f"<Category {self.category_name}>"

class Product(db.Model):
    __tablename__ = 'products'
    
    product_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_name = db.Column(db.String(255), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'), nullable=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.supplier_id'), nullable=True)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    stock_quantity = db.Column(db.Integer, nullable=False, default=0)
    reorder_level = db.Column(db.Integer, nullable=False)
    discontinued = db.Column(db.Boolean, default=False)

    # Relationships
    inventory = db.relationship('Inventory', backref='product', lazy=True)
    sales_items = db.relationship('SalesItem', backref='product', lazy=True)

    def __repr__(self):
        return f"<Product {self.product_name}>"

class Supplier(db.Model):
    __tablename__ = 'suppliers'
    
    supplier_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    supplier_name = db.Column(db.String(255), nullable=False)
    contact_name = db.Column(db.String(255), nullable=True)
    contact_email = db.Column(db.String(255), nullable=True)
    contact_phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.Text, nullable=True)

    # Relationships
    products = db.relationship('Product', backref='supplier', lazy=True)

    def __repr__(self):
        return f"<Supplier {self.supplier_name}>"


class Customer(db.Model):
    __tablename__ = 'customers'
    
    customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.Text, nullable=True)

    # Relationships
    sales = db.relationship('Sale', backref='customer', lazy=True)

    def __repr__(self):
        return f"<Customer {self.customer_name}>"

class Inventory(db.Model):
    __tablename__ = 'inventory'
    
    inventory_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)
    stock_in = db.Column(db.Integer, nullable=False)
    stock_out = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f"<Inventory Product: {self.product_id}, Stock In: {self.stock_in}, Stock Out: {self.stock_out}>"


class Sale(db.Model):
    __tablename__ = 'sales'
    
    sale_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    sale_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    payment_status = db.Column(db.Enum('Pending', 'Paid', 'Cancelled'), default='Pending')

    # Relationships
    sale_items = db.relationship('SalesItem', backref='sale', lazy=True)
    payments = db.relationship('Payment', backref='sale', lazy=True)

    def __repr__(self):
        return f"<Sale {self.sale_id} by Customer {self.customer_id}>"

class SalesItem(db.Model):
    __tablename__ = 'sales_items'
    
    sale_item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sale_id = db.Column(db.Integer, db.ForeignKey('sales.sale_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    total_price = db.Column(db.Numeric(10, 2), nullable=False)

    def __repr__(self):
        return f"<SalesItem {self.sale_item_id} - Product {self.product_id}>"

class User(db.Model,UserMixin):
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(255), nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('Admin', 'Salesperson'), default='Salesperson')
    

    # Relationships
    sales = db.relationship('Sale', backref='user', lazy=True)

    def get_id(self):
        return str(self.user_id)

    def __repr__(self):
        return f"<User {self.full_name}>"

class Payment(db.Model):
    __tablename__ = 'payments'
    
    payment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sale_id = db.Column(db.Integer, db.ForeignKey('sales.sale_id'), nullable=False)
    amount_paid = db.Column(db.Numeric(10, 2), nullable=False)
    payment_method = db.Column(db.Enum('Cash', 'Card', 'Bank Transfer'), nullable=False)
    payment_date = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f"<Payment {self.payment_id} - Sale {self.sale_id}>"
