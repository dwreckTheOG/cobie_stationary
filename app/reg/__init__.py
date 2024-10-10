from flask import Blueprint, current_app


reg_bp = Blueprint('reg', __name__, template_folder='templates')


from app.reg import routes
