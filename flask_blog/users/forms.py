from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired,Length,Email,EqualTo, ValidationError
from flask_blog.models import User
from flask_login import current_user

class RegistrationForm(FlaskForm):
    username = StringField('Username',validators = [ DataRequired(), Length(min=2,max=20) ])
    email = StringField('Email', validators = [DataRequired(),Email()])
    password = PasswordField('Password', validators = [ DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators = [ DataRequired(), Length(min=8), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self,username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError("The username already exists, Please choose another username")

    def validate_email(self,email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError("The email already exists, Please choose another email")


class LoginForm(FlaskForm):
    username = StringField('Username',validators = [ DataRequired(), Length(min=2,max=20) ])
    password = PasswordField('Password', validators = [ DataRequired(), Length(min=8)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class AccountUpdateForm(FlaskForm):
    username = StringField('Username',validators = [DataRequired(),Length(min=2,max=20) ])
    email = StringField('Email', validators = [DataRequired(),Email()])
    picture = FileField('Update Profile Picture', validators = [FileAllowed(['jpg','png','jpeg'])])
    submit = SubmitField('Save Changes')

    def validate_username(self,username):

        if current_user.username != username.data:
            user = User.query.filter_by(username = username.data).first()
            if user:
                raise ValidationError("The username already exists, Please choose another username")

    def validate_email(self,email):
        if current_user.email != email.data:
            user = User.query.filter_by(email = email.data).first()
            if user:
                raise ValidationError("The email already exists, Please choose another email")
            

class RequestResetForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired(),Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self,email):
        user = User.query.filter_by(email = email.data).first()
        if user is None:
            raise ValidationError("The email doesn't Exists, recheck the Email")


class ResetPassword(FlaskForm):
    password = PasswordField('Password', validators = [ DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators = [ DataRequired(), Length(min=8), EqualTo('password')])
    submit = SubmitField(' Reset Password ')