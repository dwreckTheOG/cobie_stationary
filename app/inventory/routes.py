from app.inventory import inventory_bp
from flask import request,render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Inventory, Product, Category, Supplier, db
from app.inventory.forms import CategoryForm, ProductForm, InventoryForm
from app.extensions import admin_required
from datetime import datetime

@inventory_bp.route('/add/inventory/<int:product_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def add_inventory(product_id):
    form = InventoryForm()

    # Populate the hidden field with the product_id
    form.product_id.data = product_id

    products = Product.query.all()
    form.product_id.choices = [(product.product_id, product.product_name) for product in products]

    # Optionally check if the product exists
    product = Product.query.get(product_id)
    if not product:
        flash('Selected product not found.', 'danger')
        return redirect(url_for('inventory.view_inventory'))

    if form.validate_on_submit():
        # Now product_id will be passed correctly as a hidden field
        stock_in = form.stock_in.data
        stock_out = form.stock_out.data

        new_stock_quantity = product.stock_quantity + stock_in - stock_out

        if new_stock_quantity < 0:
            flash('Stock cannot be negative. Please check stock-out value.', 'danger')
            return redirect(url_for('inventory.add_inventory', product_id=product_id))

        product.stock_quantity = new_stock_quantity

        new_inventory = Inventory(
            product_id=form.product_id.data,  # Use form.product_id.data here
            stock_in=stock_in,
            stock_out=stock_out,
            date=datetime.now()
        )

        try:
            db.session.add(new_inventory)
            db.session.commit()
            flash('Inventory added and stock updated successfully!', 'success')
            return redirect(url_for('inventory.view_inventory'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding inventory: {str(e)}', 'danger')
    print("Form data:", form.data)
    print("Validation errors:", form.errors)
    return render_template('add_inventory.html', form=form, product_id=product_id)


@inventory_bp.route('/update/category/<int:category_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def update_category(category_id):
    # Retrieve the category from the database
    category = Category.query.get_or_404(category_id)

    if request.method == 'POST':
        # Update category details based on the form input
        category.category_name = request.form['category_name']
        category.description = request.form['description']
        
        # Commit the changes to the database
        db.session.commit()
        flash('Category updated successfully!', 'success')
        return redirect(url_for('inventory.list_category'))  # Redirect to the list of categories

    # Render the update category form with current data
    return render_template('update_category.html', category=category)

@inventory_bp.route('/delete/category/<int:category_id>', methods=['POST'])
@login_required
@admin_required
def delete_category(category_id):
    # Retrieve the category from the database
    category = Category.query.get_or_404(category_id)

    # Delete the category
    db.session.delete(category)
    db.session.commit()
    flash('Category deleted successfully!', 'success')
    return redirect(url_for('inventory.list_category'))  # Redirect back to the list of categories

@inventory_bp.route('/manage/category')
@login_required
def list_category():
    # Check if the user has the correct role
    if current_user.role not in ['Admin']:
        flash("You don't have permission to manage categories.", 'danger')
        return redirect(url_for('inventory.view_inventory'))

    # Fetch all categories
    categories = Category.query.all()
    return render_template('list_category.html', categories=categories)

@inventory_bp.route('/add/category', methods=['GET', 'POST'])
@login_required
@admin_required
def add_category():
    # Check if the user has the correct role
    if current_user.role not in ['Admin']:
        flash("You don't have permission to add categories.", 'danger')
        return redirect(url_for('inventory.list_category'))

    form = CategoryForm()

    # If the form is submitted and valid
    if form.validate_on_submit():
        new_category = Category(
            category_name=form.category_name.data,
            description=form.description.data
        )
        # Add the category to the database
        db.session.add(new_category)
        db.session.commit()

        flash('Category added successfully!', 'success')
        return redirect(url_for('inventory.list_category'))

    return render_template('add_category.html', form=form)

@inventory_bp.route('/update/product/<int:product_id>', methods=['GET', 'POST'])
@admin_required
def update_product(product_id):
    product = Product.query.get_or_404(product_id)
    form = ProductForm(obj=product)

    # Populate the category choices
    form.category_id.choices = [(category.category_id, category.category_name) for category in Category.query.all()]
    
    # Populate the supplier choices
    form.supplier_id.choices = [(supplier.supplier_id, supplier.supplier_name) for supplier in Supplier.query.all()]

    if form.validate_on_submit():
        product.product_name = form.product_name.data
        product.product_code = form.product_code.data  # Assign product_code from the form
        product.category_id = form.category_id.data
        product.supplier_id = form.supplier_id.data
        product.unit_price = form.unit_price.data
        product.stock_quantity = form.stock_quantity.data
        product.reorder_level = form.reorder_level.data
        product.discontinued = form.discontinued.data

        try:
            db.session.commit()
            flash('Product updated successfully!', 'success')
            return redirect(url_for('inventory.view_inventory'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating product: {str(e)}', 'danger')

    return render_template('update_product.html', form=form)


@inventory_bp.route('/delete/product/<int:product_id>', methods=['GET'])
@admin_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)

    try:
        db.session.delete(product)
        db.session.commit()
        flash('Product deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting product: {str(e)}', 'danger')

    return redirect(url_for('inventory.view_inventory'))

@inventory_bp.route('/add/product', methods=['GET', 'POST'])
@login_required
@admin_required
def add_product():
    # Fetch category data for form select field
    category_data = [(c.category_id, c.category_name) for c in Category.query.all()]
    
    # Fetch supplier data for form select field
    supplier_data = [(s.supplier_id, s.supplier_name) for s in Supplier.query.all()]

    form = ProductForm()

    # Populate category and supplier choices dynamically
    form.category_id.choices = category_data
    form.supplier_id.choices = supplier_data

    # If the form is submitted and valid
    if form.validate_on_submit():
        new_product = Product(
            product_name=form.product_name.data,
            product_code=form.product_code.data,  # Include product_code
            category_id=form.category_id.data,
            supplier_id=form.supplier_id.data,
            unit_price=form.unit_price.data,
            stock_quantity=form.stock_quantity.data,
            reorder_level=form.reorder_level.data,
            discontinued=form.discontinued.data
        )
        try:
            # Add the product to the database
            db.session.add(new_product)
            db.session.commit()

            flash('Product added successfully!', 'success')
            return redirect(url_for('inventory.view_inventory'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding product: {str(e)}', 'danger')

    return render_template('add_product.html', form=form)


@inventory_bp.route('/view/inventory')
@login_required
def view_inventory():
    # Check if the user has the correct role
    if current_user.role not in ['Admin', 'Salesperson']:
        flash("You don't have permission to view the inventory.", 'danger')
        return redirect(url_for('base.index'))

    # Fetch all products with category and supplier information
    products = Product.query.all()
    categories = Category.query.all()
    suppliers = Supplier.query.all()

    # Render the inventory template with products, categories, and suppliers
    return render_template('view_inventory.html', products=products, 
    	categories=categories, suppliers=suppliers)
