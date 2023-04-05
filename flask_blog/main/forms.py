from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField
from wtforms.validators import DataRequired,Email

class Contact(FlaskForm):
    email = StringField('Email', validators = [DataRequired(),Email()])
    subject = StringField('Subject',validators = [DataRequired()])
    description = TextAreaField('Description', validators= [DataRequired()])
    submit = SubmitField('Send')