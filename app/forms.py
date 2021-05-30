'''
FloatField -- Text field that accepts a floating-point value
FormField -- Form embedded as a field in a container form
IntegerField -- Text field that accepts an integer value
PasswordField -- Password text field
RadioField -- List of radio buttons
SelectField -- Drop-down list of choices
SelectMultipleField -- Drop-down list of choices with multiple selection
SubmitField -- Form submission button
StringField -- Text field
TextAreaField -- Multiple-line text field
'''

from flask_wtf import FlaskForm
from wtforms import StringField,BooleanField,PasswordField,SubmitField,TextAreaField
from wtforms.validators import DataRequired,Length,Email,EqualTo
from app.models import User, Post


class LoginForm(FlaskForm):
	username = StringField('Username',validators=[DataRequired()])
	password = PasswordField('Password',validators=[DataRequired()])
	remember_me = BooleanField('remember_me')
	submit = SubmitField('Submit')

class RegisterForm(FlaskForm):
	username = StringField('Username',validators=[DataRequired(),Length(min=0,max=25)])
	email = StringField('Email',validators=[DataRequired(),Email()])
	password = PasswordField('Password',validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')]) #1)
	submit = SubmitField('Submit')

	def validate_username(self,username):
		user = User.query.filter_by(username=username.data).first()
		if user is not None:
			raise ValidationError('Please use a different username')

	def validate_email(self,email):
		user = User.query.filter_by(email=email.data).first()
		if user is not None:
			raise ValidationError('Please use a different Email')

class PostForm(FlaskForm):
	user_post = TextAreaField('Say Something',validators=[DataRequired()])
	submit = SubmitField('Submit')

class EditProfileForm(FlaskForm):
	username = StringField('Username',validators=[DataRequired()])
	about_me = StringField('About_me',validators=[DataRequired()])
	submit = SubmitField('Submit')

	def __init__(self,original_username, *args, **kwargs):
		super(EditProfileForm, self).__init__(*args, **kwargs)
		self.original_username = original_username

	def validate_username(self,username):
		if self.original_username != username.data:
			user = User.query.filter_by(username=username.data).first()
			if user is not None:
				raise ValidationError('Please use a different username') 

class ResetPasswordForm(FlaskForm):
	password = PasswordField('Enter New Password:', validators=[DataRequired(),EqualTo('confirm_password')])
	confirm_password = PasswordField('Confirm New Password', validators=[DataRequired()])
	submit = SubmitField('Submit')

class ForgotPasswordForm(FlaskForm):
	email = StringField('Enter Your registered email:', validators=[DataRequired(),Email()])
	submit = SubmitField('Submit')



	"""
	#1)
	class EqualTo(object):
   
    Compares the values of two fields.

    :param fieldname:
        The name of the other field to compare to.
    :param message:
        Error message to raise in case of a validation error. Can be
        interpolated with `%(other_label)s` and `%(other_name)s` to provide a
        more helpful error.
    """
