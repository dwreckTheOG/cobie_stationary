from flask import Blueprint, current_app


report_bp = Blueprint('report', __name__, template_folder='templates')


from app.report import routes
