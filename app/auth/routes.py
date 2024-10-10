from app.auth import auth_bp
from flask import render_template

@auth_bp.route('/login')
def login():
	return render_template('login.html')