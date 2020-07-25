#simiar to routes.py, but for handling error pages

from flask import Blueprint, render_template
errors = Blueprint('errors', __name__)

@errors.app_errorhandler(404)  #not found error
def error_404(error):
	return render_template('errors/404.html'), 404

@errors.app_errorhandler(403)  #forbidden request error
def error_403(error):
	return render_template('errors/403.html'), 403

@errors.app_errorhandler(500)  #general database error
def error_500(error):
	return render_template('errors/500.html'), 500