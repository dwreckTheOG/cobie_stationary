from app.extensions import db
from flask_login import UserMixin
from sqlalchemy import LargeBinary
from enum import Enum

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
    product_code = db.Column(db.String(10), unique=True, nullable=True)  # New field for product code
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'), nullable=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.supplier_id'), nullable=True)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    stock_quantity = db.Column(db.Integer, nullable=False, default=0)
    reorder_level = db.Column(db.Integer, nullable=False)
    discontinued = db.Column(db.Boolean, default=False)
    image = db.Column(LargeBinary, nullable=True)  # New field for storing image data

    # Relationships
    inventory = db.relationship('Inventory', backref='product', lazy=True)
    sales_items = db.relationship('SalesItem', backref='product', lazy=True)

    def __repr__(self):
        return f"<Product {self.product_name}>"

    @classmethod
    def update_by_product_code(cls, product_code, **kwargs):
        """Update a product record by product code.
        
        Args:
            product_code (str): The product code of the product to update.
            **kwargs: The fields to update (e.g., product_name, unit_price, stock_quantity, etc.).
        
        Returns:
            bool: True if the update was successful, False otherwise.
        """
        product = cls.query.filter_by(product_code=product_code).first()
        if not product:
            return False  # Product not found
        
        for key, value in kwargs.items():
            if hasattr(product, key):
                setattr(product, key, value)
        
        db.session.commit()  # Commit the changes
        return True  # Update successful

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
    password = db.Column(db.String(255), nullable=True)

    # Relationships
    sales = db.relationship('Sale', backref='customer', lazy=True)
    cart = db.relationship('Cart', backref='customer', uselist=False)  # Each customer can have one cart
    orders = db.relationship('Order', backref='customer', lazy=True)  # Each customer can have many orders

    def __repr__(self):
        return f"<Customer {self.customer_name}>"
    
    def get_id(self):
        return str(self.customer_id)

    # Flask-Login required methods
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True  # You can add additional logic if you need to control this

    @property
    def is_anonymous(self):
        return False


class Inventory(db.Model):
    __tablename__ = 'inventory'
    
    inventory_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)
    stock_in = db.Column(db.Integer, nullable=True)
    stock_out = db.Column(db.Integer, nullable=True)
    date = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f"<Inventory Product: {self.product_id}, Stock In: {self.stock_in}, Stock Out: {self.stock_out}>"

class Sale(db.Model):
    __tablename__ = 'sales'
    
    sale_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    sale_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    total_amount = db.Column(db.Numeric(10, 2), nullable=True)
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
    product_code = db.Column(db.String(50), db.ForeignKey('products.product_code'), nullable=False)  # Reference by product_code
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Numeric(10, 2), nullable=False)

    def __repr__(self):
        return f"<SalesItem {self.sale_item_id} - Product {self.product_code}>"


class User(db.Model, UserMixin):
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
    sale_id = db.Column(db.Integer, db.ForeignKey('sales.sale_id'), nullable=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'), nullable=True)  # Add order_id field
    amount_paid = db.Column(db.Numeric(10, 2), nullable=False)
    payment_method = db.Column(db.Enum('Cash', 'M-Pesa'), nullable=False)
    payment_date = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f"<Payment {self.payment_id} - Sale {self.sale_id} - Order {self.order_id}>"



class CartStatus(Enum):
    PENDING = 'pending'
    ORDERED = 'ordered'

class Cart(db.Model):
    __tablename__ = 'carts'
    
    cart_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id'), nullable=False)
    status = db.Column(db.Enum(CartStatus), nullable=False, default=CartStatus.PENDING)  # Adding status column
    
    # Relationships
    cart_items = db.relationship('CartItem', backref='cart', lazy=True)

    def __repr__(self):
        return f"<Cart {self.cart_id} for Customer {self.customer_id} - Status: {self.status.value}>"


class CartItem(db.Model):
    __tablename__ = 'cart_items'
    
    cart_item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('carts.cart_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    # Define relationship to Product
    product = db.relationship('Product', backref='cart_items', lazy=True)

    def __repr__(self):
        return f"<CartItem {self.cart_item_id} - Product {self.product_id}, Quantity {self.quantity}>"

class Order(db.Model):
    __tablename__ = 'orders'
    
    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id'), nullable=False)
    order_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.Enum('Pending','Sorting','Transporting', 'Completed', 'Cancelled'), default='Pending')

    # Relationships
    order_items = db.relationship('OrderItem', backref='order', lazy=True)

    def __repr__(self):
        return f"<Order {self.order_id} by Customer {self.customer_id}>"

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    
    order_item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Numeric(10, 2), nullable=False)

    # Define relationship with Product
    product = db.relationship('Product', backref='order_items')

    def __repr__(self):
        return f"<OrderItem {self.order_item_id} - Product {self.product_id}, Quantity {self.quantity}>"
