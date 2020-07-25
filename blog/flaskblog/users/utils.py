#blueprinting for better modular structure
#will contain FUNCTIONS related to users

import os        # for saving image
import secrets   # for naming image randomly in hex
from PIL import Image  #import pillow library functionality
from flask import url_for, current_app
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import mail
from flask_mail import Message 
#IMPORTANT: 'less secure app access' must be enabled in Gmail account for mail to be sent at all


def save_picture(form_picture):
	random_hex = secrets.token_hex(8)   #create random hex name for img to be saved in database
	_, f_ext = os.path.splitext(form_picture.filename) #obtain filename and extension
	pic_file_name = random_hex + f_ext
	picture_path = os.path.join(current_app.root_path, 'static/profile_pics', pic_file_name)
	
	output_size = (125, 125)
	resized_pic = Image.open(form_picture) #open pic, not resized yet
	resized_pic.thumbnail(output_size) #resize to 125x125 for easy storage in database
	resized_pic.save(picture_path)
	
	old_pic = current_user.image_file     #delete previous image from database
	if old_pic != 'default.jpg':
		os.remove(os.path.join(current_app.root_path, 'static/profile_pics', old_pic))
	
	return pic_file_name


def send_reset_email(user):
	token = user.get_reset_token()
	msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
	
	msg.body = f''' To reset your password, visit the following link which expires in 5 minutes:
{url_for('users.reset_token', token=token, _external=True)} 

If you did not make this request, then please ignore this mail and no changes will be made.
''' #'_external' to specify it will be an absolute URL, triple" ' " to specify multiline string

	mail.send(msg)
