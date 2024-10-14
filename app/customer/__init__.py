from flask import Blueprint, current_app


customer_bp = Blueprint('customer', __name__, template_folder='templates')


from app.customer import routes
