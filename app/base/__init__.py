from flask import Blueprint, current_app


base_bp = Blueprint('base', __name__, template_folder='templates')


from app.base import routes
