#blueprinting for betetr modular structure
#will contain forms related to functionalities for posts

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
	title = StringField('Title', validators=[DataRequired()])
	
	content = TextAreaField('Content', validators=[DataRequired()])

	submit = SubmitField('Post')
