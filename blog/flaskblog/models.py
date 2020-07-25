from itsdangerous import TimedJSONWebSignatureSerializer as Serializer #for OTP token
from datetime import datetime
from flaskblog import db, login_manager
from flask_login import UserMixin
from flask import current_app

@login_manager.user_loader   #declare as decorator
def load_user(user_id):      #for login_manager extension
	return User.query.get(int(user_id))


class User(db.Model, UserMixin):      #Inherit from model and usermixin classes
	id = db.Column(db.Integer, primary_key=True)  #make id column
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	image_file = db.Column(db.String(20), nullable=False, default='default.jpg')  #profile pic
	password = db.Column(db.String(60), nullable=False)

	posts = db.relationship('Post', backref='author', lazy=True) #def many one relation for user

	def __repr__(self):  # tells how object is printed in database (just for analysis)
		return f"User('{self.username}', '{self.email}', '{self.image_file}')"

	def get_reset_token(self, expires_sec=1800):               #expires in 1800 sec 
		s = Serializer(current_app.config['SECRET_KEY'], expires_sec)  #serializer object 's'
		return s.dumps({'user_id':self.id}).decode('utf-8')    #return expirable token
															   #uses user_id from parent user class
						#returns token to email function, so that token can be made into a reset link

	@staticmethod                       #tell python that this method does not take self argument
	def verify_reset_token(token):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			user_id = s.loads(token)['user_id'] #s.loads returns dictionary defined inside get_reset-
												#function, which expires within some defined time
												#FINAL STEP OF VERIFICATION using token
			return User.query.get(user_id)
		except:
			return None                         #if token invalid or expired, etc.


class Post(db.Model):                  #Table for Posts
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	content = db.Column(db.Text, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) #reference tablename 'user'

	def __repr__(self):
		return f"Post('{self.title}, '{self.date_posted}')"