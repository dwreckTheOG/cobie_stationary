from flask import Blueprint, current_app


inventory_bp = Blueprint('inventory', __name__, template_folder='templates')


from app.inventory import routes
