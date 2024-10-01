from app.base import base_bp
from flask import render_template

@base_bp.route('/')
def index():
	return render_template('index.html')