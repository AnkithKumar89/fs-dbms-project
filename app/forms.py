import email
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import Faculty


class LoginForm(FlaskForm):
	username=StringField('Username',validators=[DataRequired()])
	password=PasswordField('Password',validators=[DataRequired()])
	remember_me=BooleanField('Remember me')
	submit=SubmitField('Sign in')

class RegistrationForm(FlaskForm):
	username = StringField('FacultyName', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Register')
	
	def validate_username(self, username):
		faculty_user = Faculty.query.filter_by(username=username.data).first()
		if faculty_user is not None:
			raise ValidationError('Please use a different name.')
	def validate_email(self, email):
		faculty_user = Faculty.query.filter_by(email=email.data).first()
		if faculty_user is not None:
			raise ValidationError('Please use a different email address.')
