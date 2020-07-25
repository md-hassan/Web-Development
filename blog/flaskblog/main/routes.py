#blueprinting for better modular structure
#will contain routes related to miscellaneous functionalities

from flask import render_template, request
from flaskblog.models import Post

from flask import Blueprint

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")                 # 2 routes being handled by same function, for same template
def home():
	page = request.args.get('page', default=1, type=int)#will return pg no. req by iter_pages
	posts = Post.query.order_by(Post.date_posted.desc()).paginate(
	page=page, per_page=5)  #paginate to display less posts per page
	return render_template('home.html', posts=posts)    # render sends mentioned stuff to html file
										     # so that posts(green one) can be accessed in template
@main.route('/about')
def about():
	return render_template('about.html', title='About')
