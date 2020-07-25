#blueprinting for better modular structure
#will contain forms related to functionalities for user

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed  # foruploading images
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User

class RegistrationForm(FlaskForm):
	username = StringField('Username', validators = [DataRequired(), Length(min = 2, max =20)])

	email = StringField('Email', validators = [DataRequired(), Email()])

	password = PasswordField('Password', validators = [DataRequired()])
	confirm_password = PasswordField('Confirm Password',
										validators = [DataRequired(), EqualTo('password')])

	submit = SubmitField('Sign Up')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first() #'first' so that returns a string
		if user:                                     #will be empty if username doesn't exist already
			raise ValidationError('Username already taken. Please choose another.')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('Email already taken. Please choose another.')


class LoginForm(FlaskForm):
	email = StringField('Email', validators = [DataRequired(), Email()])

	password = PasswordField('Password', validators = [DataRequired()])
	
	remember = BooleanField('Remember Me')

	submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])

	email = StringField('Email', validators=[DataRequired(), Email()])

	picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])

	submit = SubmitField('Update')

	def validate_username(self, username):
		if username.data != current_user.username:  #if username is different, then check availability
			user = User.query.filter_by(username=username.data).first()
			if user:
				raise ValidationError('Username already taken. Please choose another.')

	def validate_email(self, email):
		if email.data != current_user.email:
			email = User.query.filter_by(email=email.data).first()
			if email:
				raise ValidationError('Email already taken. Please choose another.')
				
class RequestResetForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])

	submit = SubmitField('Request Password Reset')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is None:
			 raise ValidationError('There is no email with that account. You must register first.')
			 #flash('There is no email with that account. You must register first.', 'warning')
			 #return redirect(url_for('users.register'))

class ResetPasswordForm(FlaskForm):
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password',
						validators=[DataRequired(), EqualTo('password')])

	submit = SubmitField('Reset Password')