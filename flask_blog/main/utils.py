from flask_blog import mail
from flask_mail import Message
import os

def send_feedback_email(form):
    msg = Message(form.subject.data,
                  sender = "feedback@demo.com",
                  recipients=[os.environ.get('EMAIL')])
    msg.body = f''' A message recieved from <{form.email.data}>
Message Body
{form.description.data}
'''
    mail.send(msg)
