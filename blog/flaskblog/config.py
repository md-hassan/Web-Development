#save all configurations here
#will allow us to do stuff like inheritance, create multiple instances of application, etc.


#grab anything with 'app.config' from flaskblog __init__ file and save here
#remove 'app.config' part and save inly the keys indide the class below

class Config:
	SECRET_KEY = 'onci1881h91y7dqdom19u01iei'         #random string
	SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'     #'///' is relative path in sqlite
	MAIL_SERVER = 'smtp.googlemail.com'
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_USERNAME = 'someemailaddress@gmail.com'  #this will be the sender
	MAIL_PASSWORD = 'somepassword'
