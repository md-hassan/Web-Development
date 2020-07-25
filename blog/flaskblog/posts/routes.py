#blueprinting for better modular structure
#will contain routes related to functionalities for posts

from flask import Flask, render_template, url_for, flash, redirect, request, abort
from flaskblog.models import Post                         #import from the package 'flaskblog'
from flaskblog.posts.forms import PostForm   			  #import from posts.forms
from flaskblog import db
from flask_login import current_user, login_required

from flask import Blueprint

posts = Blueprint('posts', __name__)

@posts.route('/post/new', methods=['POST','GET'])
@login_required
def new_post():
	form = PostForm()
	if form.validate_on_submit():
		post = Post(title=form.title.data, content=form.content.data, author=current_user)
		db.session.add(post)
		db.session.commit()
		flash('Post created!', 'success')
		return redirect(url_for('main.home'))
	return render_template('create_or_update_post.html', title='New Post',
						  form=form, legend='New Post') #legend defined to diff b/w update/create
						  								# since they both use the same template 
						  								
@posts.route('/post/<post_id>')
def post(post_id):
	post = Post.query.get_or_404(post_id)   #return page or 404 error if post_id DNE
	return render_template('post.html', title=post.title, post=post)

@posts.route('/post/<post_id>/update', methods=['POST', 'GET'])
@login_required
def update_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)                          #403 is forbidden route	
	form = PostForm()
	if form.validate_on_submit():
		post.title = form.title.data
		post.content = form.content.data
		db.session.commit()
		flash('Post updated!', 'success')
		return redirect(url_for('posts.post', post_id=post.id))
	elif request.method == 'GET':#On openeing page, automatically fill form using existing post data
		form.title.data = post.title
		form.content.data = post.content
	return render_template('create_or_update_post.html', title='Update Post',
							 form=form, legend='Update Post')

@posts.route('/post/<post_id>/delete', methods=['POST'])#GET not req,only need POST for delete rquests
@login_required
def delete_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)
	db.session.delete(post)
	db.session.commit()
	flash('Post deleted!', 'success')
	return redirect(url_for('main.home'))

