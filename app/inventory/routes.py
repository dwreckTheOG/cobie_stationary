from app.inventory import inventory_bp
from flask import request,render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Product, Category, Supplier, db
from app.inventory.forms import CategoryForm, ProductForm, InventoryForm

@inventory_bp.route('/update/category/<int:category_id>', methods=['GET', 'POST'])
@login_required
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


@inventory_bp.route('/add/product', methods=['GET', 'POST'])
@login_required
def add_product():
    # Fetch category data
    category_data = Category.query.all()

    # Fetch supplier data
    supplier_data = Supplier.query.all()

    # Check if the user has the correct role
    if current_user.role not in ['Admin']:
        flash("You don't have permission to add products.", 'danger')
        return redirect(url_for('inventory.view_inventory'))

    form = ProductForm()

    # If the form is submitted and valid
    if form.validate_on_submit():
        new_product = Product(
            product_name=form.product_name.data,
            category_id=form.category_id.data,
            supplier_id=form.supplier_id.data,
            unit_price=form.unit_price.data,
            stock_quantity=form.stock_quantity.data,
            reorder_level=form.reorder_level.data,
            discontinued=form.discontinued.data
        )
        # Add the product to the database
        db.session.add(new_product)
        db.session.commit()

        flash('Product added successfully!', 'success')
        return redirect(url_for('inventory.view_inventory'))

    return render_template('add_product.html', form=form, categories=category_data, suppliers=supplier_data)


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
