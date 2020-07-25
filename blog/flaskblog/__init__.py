# Meant to initialise/import req stuff
# MAKING AN __init__ FILE SPECIFES THAT THE FOLDER IS A PACKAGE
# Package for database
# THIS FILE IS REFERRED TO AS 'flaskblog' by other modules

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager    #extension to handle logins
from flask_mail import Mail
from flaskblog.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()  #initialize to encrypt password
login_manager = LoginManager() #initialize login manager
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'  #bootstrap for 'login access this page' message box 
mail = Mail()   #initialize mail


def create_app(config_classs=Config): #to create new instances of application 
	app = Flask(__name__)
	app.config.from_object(Config)   #use configurations from config file
	
	#from flaskblog import routes      #done after 'app' initialisation to avoid circular import problem
	#👆above code removed due to blueprinting
	#replacement is below

	from flaskblog.users.routes import users #importing instance of blueprint 'users'
	from flaskblog.posts.routes import posts
	from flaskblog.main.routes import main
	from flaskblog.errors.handlers import errors

	app.register_blueprint(users)            #register that as a blueprint
	app.register_blueprint(posts)  
	app.register_blueprint(main)
	app.register_blueprint(errors)

	#extensions not moved here. remain outside create_app function. but we can call them to 
	#to initalize those extensions like below:
	#done so that same extansions can used for other instances as well 

	db.init_app(app)
	bcrypt.init_app(app)
	login_manager.init_app(app)
	mail.init_app(app)

	return app