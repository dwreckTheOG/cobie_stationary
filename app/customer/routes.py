from flask import session, render_template, redirect, url_for, flash, request, abort
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from app.customer import customer_bp
from app.models import CartStatus,Customer, Product, Cart, CartItem, Order, OrderItem
from app.customer.forms import CustomerRegistrationForm, CustomerLoginForm
from app.extensions import db
import random

@customer_bp.route('/customer/register', methods=['GET', 'POST'])
def customer_register():
    form = CustomerRegistrationForm()
    if form.validate_on_submit():
        existing_customer = Customer.query.filter_by(email=form.email.data).first()
        if existing_customer:
            flash('Email already registered. Please log in.', 'error')
            return redirect(url_for('customer.customer_login'))

        hashed_password = generate_password_hash(form.password.data)
        new_customer = Customer(
            customer_name=form.customer_name.data,
            email=form.email.data,
            phone=form.phone.data,
            address=form.address.data,
            password=hashed_password
        )
        
        db.session.add(new_customer)
        db.session.commit()

        login_user(new_customer)
        session['user_type'] = 'customer'
        flash('Registration successful! Welcome!', 'success')
        return redirect(url_for('customer.customer_dashboard'))
    
    return render_template('customer_register.html', form=form)

@customer_bp.route('/customer/login', methods=['GET', 'POST'])
def customer_login():
    form = CustomerLoginForm()
    if form.validate_on_submit():
        customer = Customer.query.filter_by(email=form.email.data).first()
        if customer and check_password_hash(customer.password, form.password.data):
            session['user_type'] = 'customer'
            login_user(customer)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('customer.customer_dashboard'))
        else:
            flash('Invalid email or password.', 'error')
    
    return render_template('customer_login.html', form=form)

@customer_bp.route('/customer/dashboard')
@login_required
def customer_dashboard():
    if session.get('user_type') != 'customer':
        abort(403)
    # Fetch orders, cart items, etc.
    orders = Order.query.filter_by(customer_id=current_user.customer_id).all()
    products = Product.query.filter_by(discontinued=False).all()
    random.shuffle(products)
    return render_template('customer_dashboard.html', orders=orders, products=products)

@customer_bp.route('/customer/logout')
@login_required
def customer_logout():
    logout_user()
    session.pop('user_type', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('customer.customer_login'))

# Route to browse available products
@customer_bp.route('/customer/products', methods=['GET'])
def browse_products():
    products = Product.query.filter_by(discontinued=False).all() 
    random.shuffle(products) # Fetch non-discontinued products
    return render_template('browse_products.html', products=products)

# Route to add a product to the cart
@customer_bp.route('/add_to_cart/<int:product_id>', methods=['GET', 'POST'])
def add_to_cart(product_id):
    # Check if the user is authenticated
    if not current_user.is_authenticated:
        return redirect(url_for('customer.customer_login'))

    # Check if the user is authenticated but is not a customer
    if session.get('user_type') != 'customer':
        logout_user()  # Log out the current user
        flash('You need to log in as a customer to add items to the cart.', 'warning')
        return redirect(url_for('customer.customer_login'))

    # Fetch the product to add to the cart
    product = Product.query.get_or_404(product_id)

    # Retrieve or create a new cart for the current customer
    cart = Cart.query.filter_by(customer_id=current_user.customer_id, status=CartStatus.PENDING).first()

    if not cart:
        # Create a new cart if no pending cart exists
        cart = Cart(customer_id=current_user.customer_id, status=CartStatus.PENDING)
        db.session.add(cart)
        db.session.commit()  # Commit to get the cart ID before adding items

    # Check if the product is already in the cart
    cart_item = CartItem.query.filter_by(cart_id=cart.cart_id, product_id=product_id).first()
    if cart_item:
        cart_item.quantity += 1  # Increment quantity if the product is already in the cart
    else:
        # Create a new cart item if not present
        cart_item = CartItem(cart_id=cart.cart_id, product_id=product_id, quantity=1)
        db.session.add(cart_item)

    db.session.commit()  # Commit the changes
    flash(f'{product.product_name} has been added to your cart.', 'success')

    return redirect(url_for('customer.browse_products'))  # Redirect to the cart view

@customer_bp.route('/customer/cart', methods=['GET'])
@login_required
def view_cart():
    # Retrieve active and pending carts for the logged-in customer
    active_cart = Cart.query.filter_by(customer_id=current_user.customer_id, status=CartStatus.ORDERED).first()
    pending_carts = Cart.query.filter_by(customer_id=current_user.customer_id, status=CartStatus.PENDING).all()

    # Active cart items
    active_cart_items = CartItem.query.filter_by(cart_id=active_cart.cart_id).all() if active_cart else []
    
    # Calculate grand total for the active cart
    active_cart_total = sum(item.quantity * item.product.unit_price for item in active_cart_items)

    # Pending cart items and total calculation
    pending_cart_items = []
    grand_total_pending = 0
    for pending_cart in pending_carts:
        items = CartItem.query.filter_by(cart_id=pending_cart.cart_id).all()
        pending_cart_items.extend(items)
        grand_total_pending += sum(item.quantity * item.product.unit_price for item in items)
    
    return render_template(
        'view_cart.html',
        pending_cart_items=pending_cart_items,
        grand_total_pending=grand_total_pending
    )


# Route to place an order
@customer_bp.route('/customer/cart/checkout', methods=['POST'])
@login_required
def checkout():
    cart = Cart.query.filter_by(customer_id=current_user.customer_id, status=CartStatus.PENDING).first()
    if not cart or not cart.cart_items:
        flash('Your cart is empty!', 'error')
        return redirect(url_for('customer.view_cart'))

    total_amount = sum(item.product.unit_price * item.quantity for item in cart.cart_items)

    # Create an order
    order = Order(customer_id=current_user.customer_id, total_amount=total_amount)
    db.session.add(order)
    db.session.commit()

    # Add order items
    for item in cart.cart_items:
        order_item = OrderItem(order_id=order.order_id, product_id=item.product_id, quantity=item.quantity, total_price=item.quantity * item.product.unit_price)
        db.session.add(order_item)

    # Update cart status to 'ordered'
    cart.status = CartStatus.ORDERED
    db.session.commit()

    flash('Order placed successfully!', 'success')
    return redirect(url_for('customer.customer_dashboard'))

# Route to view order history
@customer_bp.route('/customer/orders', methods=['GET', 'POST'])  # Corrected this line
@login_required
def view_orders():
    orders = Order.query.filter_by(customer_id=current_user.customer_id).all()
    return render_template('view_orders.html', orders=orders)
