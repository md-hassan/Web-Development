#blueprinting for better modular structure
#will contain routes related to functionalities for user

from flask import Flask, render_template, url_for, flash, redirect, request, abort
from flaskblog.models import User, Post                    #import from the package 'flaskblog'
from flaskblog import db, bcrypt, mail
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog.users.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flaskblog.users.forms import RequestResetForm, ResetPasswordForm #import from users.forms
from flaskblog.users.utils import save_picture, send_reset_email


from flask import Blueprint

users = Blueprint('users', __name__) #declare blueprint with name 'users'

@users.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:			#if logged in, redirect to home
		return redirect(url_for('main.home'))

	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8') #hash pw
		user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
																		#create user in database
		db.session.add(user)     #add to database
		db.session.commit()      #commit to database

		flash(f'Account created for {form.username.data}! You can now Login.',
				'success')  #f means variable in flash msg, success tells type of message
		return redirect(url_for('users.login'))
	return render_template('register.html', title='Register', form=form)

@users.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))

	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):#check if user 
																		#exists and verify password
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')  #if trying to access 'logged-in' only pages, user will
			#get redirected to login page and next page on stack will be the previous 'logged-in' page
			flash('Logged in.', 'success')
			if next_page:
				return redirect(next_page)
			else:
				return redirect(url_for('main.home'))
		else:
			flash('Login unsuccessful. Please check credentials.', 'danger')
	return render_template('login.html', title='Login', form=form)

@users.route('/logout')
def logout():
	logout_user()
	flash('Logged out', 'success')
	return redirect(url_for('main.home'))

@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
	form = UpdateAccountForm()
	if form.validate_on_submit():
		if form.picture.data:
			picture_file = save_picture(form.picture.data)
			current_user.image_file = picture_file

		current_user.username = form.username.data
		current_user.email = form.email.data

		db.session.commit() #save changes to database
		flash('Your account has been updated!', 'success')
		return redirect(url_for('users.account'))

	elif request.method == 'GET':#Automatically fill form using existing data when simply loading page
		form.username.data = current_user.username        #since GET is default request?
		form.email.data = current_user.email

	image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
	return render_template('account.html', title='Account', image_file=image_file, form=form)

@users.route('/user/<string:username>')
def user_post(username):     # to display all posts by that author
	page = request.args.get('page', default=1, type=int)
	user = User.query.filter_by(username=username).first_or_404() #get user_id
	posts = Post.query.filter_by(author=user)\
			.order_by(Post.date_posted.desc())\
			.paginate(page=page, per_page=5)
	return render_template('user_post.html', posts=posts, user=user)


@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
	if current_user.is_authenticated:         #if logged in, redirect user to home
		return redirect(url_for('main.home'))
	form = RequestResetForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		send_reset_email(user)
		flash('Email for password reset sent! Check your inbox.', 'info')
		return redirect(url_for('users.login'))
	return render_template('reset_request.html', title='Reset Password', form=form)

@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	user = User.verify_reset_token(token)   #function defined under User model, returns User object
	if user is None:
		flash('That is an invalid or expired token', 'warning')
		return redirect(url_for('users.reset_request'))
	form = ResetPasswordForm()
	if form.validate_on_submit():
		hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8') #hash pw
		user.password = hashed_pw									#update password in database
		db.session.commit()      #commit to database

		flash(f'Password succesfully reset! You can now Login.',
				'success')  
		return redirect(url_for('users.login'))
	return render_template('reset_token.html', title='Reset Password', form=form)