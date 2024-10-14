from flask import request, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import OrderItem,Order,Payment,Customer,Product, Sale, SalesItem  # Make sure to import your models
from app.order import order_bp
from app.order.forms import PaymentForm,OrderStatusForm

# Route to finalize an order
@order_bp.route('/checkout/<int:order_id>', methods=['GET', 'POST'])
@login_required
def checkout(order_id):
    order = Order.query.get_or_404(order_id)

    # Retrieve the total amount for the order
    total_amount = order.total_amount

    # Check if payment details are submitted
    form = PaymentForm()
    if form.validate_on_submit():
        # Capture sale_id and order_id from the form
        sale_id = form.sale_id.data
        order_id = form.order_id.data  # This should match the route parameter

        # Check the amount paid
        amount_paid = form.amount_paid.data

        # Validation logic for payment
        if amount_paid > total_amount:
            flash('Amount paid cannot exceed the total amount.', 'error')
            return render_template('checkout.html', form=form, order=order, total_amount=total_amount)

        # Update order status based on payment
        if amount_paid == total_amount:
            # Deduct quantities from products in stock
            order_items = OrderItem.query.filter_by(order_id=order_id).all()
            for item in order_items:
                product = Product.query.get(item.product_id)  # Retrieve the product directly
                if product:
                    # Check if there's enough stock
                    if product.stock_quantity < item.quantity:
                        flash(f'Insufficient stock for {product.product_name}.', 'error')
                        db.session.rollback()  # Rollback on error
                        return redirect(url_for('order.view_customer_orders'))

                    # Subtract the sold quantity from the stock
                    product.stock_quantity -= item.quantity

            # Create a new payment record
            payment = Payment(
                sale_id=sale_id,  # Captured from the form
                order_id=order_id,  # Captured from the form
                amount_paid=amount_paid,
                payment_method=form.payment_method.data,
                payment_date=form.payment_date.data
            )
            db.session.add(payment)

            # Mark the order as completed
            order.status = 'Completed'
            db.session.commit()

            flash('Order completed successfully!', 'success')
            return redirect(url_for('order.view_customer_orders'))  # Redirect to an appropriate page after checkout
        else:
            flash('Payment received, but not sufficient to complete the order.', 'warning')

    # Render the checkout page with the form and total amount
    return render_template('checkout.html', form=form, order=order, total_amount=total_amount)

@order_bp.route('/order/<int:order_id>', methods=['GET'])
@login_required
def view_order_details(order_id):
    form = OrderStatusForm()
    # Retrieve the order by ID
    order = Order.query.get_or_404(order_id)

    # Get the order items
    order_items = order.order_items

    return render_template('view_order_details.html',
    form=form, order=order, order_items=order_items)


@order_bp.route('/order/update_status/<int:order_id>', methods=['GET', 'POST'])
@login_required
def update_order_status(order_id):
    # Retrieve the order by ID
    order = Order.query.get_or_404(order_id)

    form = OrderStatusForm()

    # Handle form submission
    if form.validate_on_submit():
        new_status = form.status.data

        # Update the order status
        order.status = new_status
        db.session.commit()

        flash(f'Order status updated to {new_status} successfully!', 'success')
        return redirect(url_for('order.view_customer_orders'))

    # Pre-fill the form with the current status
    form.status.data = order.status

    return render_template('update_order_status.html', form=form, order=order)


# Route to view a specific customer's order history
@order_bp.route('/customer/orders', methods=['GET'])
@login_required
def view_customer_orders():
    orders = Order.query.all()
    return render_template('view_orders.html', orders=orders)


# Route to finalize an order
@order_bp.route('/finalize/order', methods=['POST'])
@login_required
def finalize_order():
    sale_id = request.form.get('sale_id')
    sale = Sale.query.get(sale_id)

    if not sale:
        flash('Sale not found.', 'error')
        return redirect(url_for('order.customer_order'))

    # Check if payment details are submitted
    form = PaymentForm()
    if form.validate_on_submit():
        # Retrieve the total amount for the sale
        total_amount = sale.total_amount  # Accessing the total_amount directly from the sale object
        
        # Check the amount paid
        amount_paid = form.amount_paid.data
        
        # Validation logic for payment
        if amount_paid > total_amount:
            flash('Amount paid cannot exceed the total amount.', 'error')
            return render_template('pay.html', form=form, sale=sale, total_amount=total_amount)
        
        # Create a new payment instance
        payment = Payment(
            sale_id=sale_id,
            amount_paid=amount_paid,
            payment_method=form.payment_method.data,
            payment_date=form.payment_date.data
        )

        # Save the payment to the database
        db.session.add(payment)

        # Update sale status based on payment
        if amount_paid == total_amount:
            # Subtract quantities from products in stock
            sales_items = SalesItem.query.filter_by(sale_id=sale_id).all()
            for item in sales_items:
                product = Product.query.filter_by(product_code=item.product_code).first()  # Query using product_code
                if product:
                    # Log current stock and the quantity being sold
                    print(f"Current stock for {product.product_name}: {product.stock_quantity}, Quantity sold: {item.quantity}")
                    
                    # Check if there's enough stock
                    if product.stock_quantity < item.quantity:
                        flash(f'Insufficient stock for {product.product_name}.', 'error')
                        db.session.rollback()  # Rollback on error
                        return redirect(url_for('order.customer_order'))
                    
                    # Subtract the sold quantity from the stock
                    new_stock_quantity = product.stock_quantity - item.quantity
                    
                    # Update the product's stock_quantity
                    success = Product.update_by_product_code(
                        item.product_code,
                        stock_quantity=new_stock_quantity  # Only pass the stock_quantity update
                    )
                    if not success:
                        flash(f"Failed to update stock for {product.product_name}.", 'error')
                        db.session.rollback()
                        return redirect(url_for('order.customer_order'))

            # Mark the sale as completed
            sale.status = 'completed'
            sale.payment_status = 'Paid'
        else:
            # Do not update the status if the amount is less than the total amount
            flash('Payment received, but not sufficient to complete the order.', 'warning')

        # Commit changes
        try:
            db.session.commit()
            flash('Payment processed successfully!', 'success')
            return redirect(url_for('order.customer_order'))  # Redirect to an appropriate page after payment
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred while processing payment: {str(e)}', 'error')
            return redirect(url_for('order.customer_order'))

    # Retrieve total amount from the sale if payment validation fails
    total_amount = sale.total_amount  # Accessing the total_amount directly from the sale object

    # If payment validation fails, render the payment page again
    return render_template('pay.html', form=form, sale=sale, total_amount=total_amount)



# Route to add a sales item to an order
@order_bp.route('/add/sale/item', methods=['POST'])
@login_required
def add_sales_item():
    sale_id = request.form.get('sale_id')
    product_id = request.form.get('product_id')
    quantity = int(request.form.get('quantity'))

    # Fetch the product using the product_id
    product = Product.query.get(product_id)
    if not product:
        flash('Product not found.', 'error')
        return redirect(url_for('order.customer_order'))

    # Calculate total price for this item
    total_price = product.unit_price * quantity  # Assuming `unit_price` is a field in the Product model

    # Create a new SalesItem instance
    new_sales_item = SalesItem(
        sale_id=sale_id,
        product_code=product.product_code,  # Use product_code instead of product_id
        quantity=quantity,
        total_price=total_price
    )

    # Add the new sales item to the session and commit
    db.session.add(new_sales_item)

    # Update the total amount for the sale
    sale = Sale.query.get(sale_id)
    if sale:
        sale.total_amount += total_price  # Update total amount
        sale.customer_id = request.form.get('customer_id')
        db.session.commit()
        flash('Sales item added successfully!', 'success')
    else:
        flash('Sale not found, item could not be added.', 'error')

    return redirect(url_for('order.customer_order'))

# Route to handle customer order creation and display
@order_bp.route('/customer/order', methods=['GET', 'POST'])
@login_required
def customer_order():
    # Check for existing pending sales for the current user
    existing_sale = Sale.query.filter_by(user_id=current_user.user_id, payment_status='Pending').first()

    if existing_sale:
        # If a pending sale exists, use that sale_id
        sale_id = existing_sale.sale_id
    else:
        # Create a new Sale record if no pending sale exists
        new_sale = Sale(user_id=current_user.user_id, total_amount=0, payment_status='Pending')  # Add status as needed
        db.session.add(new_sale)
        db.session.commit()
        sale_id = new_sale.sale_id

    # Retrieve the sales items for the current sale
    order_items = SalesItem.query.filter_by(sale_id=sale_id).all()

    # Calculate total_amount based on SalesItems
    total_amount = sum(item.total_price for item in order_items)
    if existing_sale:
        existing_sale.total_amount = total_amount
    else:
        new_sale.total_amount = total_amount

    db.session.commit()

    # Fetch products for the dropdown
    products = Product.query.all()

    sale = Sale.query.filter_by(sale_id=sale_id)

    customers = Customer.query.all()
    return render_template('customer_order.html', sale_id=sale_id,
     order_items=order_items, products=products,
     customers=customers)
