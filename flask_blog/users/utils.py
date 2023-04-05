from flask_mail import Message
from PIL import Image
import os,secrets
from flask_login import current_user
from flask_blog import mail
from flask import url_for,current_app

def save_picture(form_picture):
    # Deleting the Old Profile Picture of the User
    old_pic = current_user.image_file
    if old_pic != 'default.jpg':
        old_picture_path = os.path.join(current_app.root_path,'static/profile_pics/',old_pic)
        if os.path.exists(old_picture_path):
            os.remove(old_picture_path)

    # Randomizing the name of profile pic and creating its path
    picture_fname = secrets.token_hex(8)
    _,f_ext = os.path.splitext(form_picture.filename)
    picture_name = picture_fname + f_ext
    picture_path = os.path.join(current_app.root_path,'static/profile_pics/',picture_name)

    # Resizing the profile picture and then saving
    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_name


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender = 'noreply@demo.com', recipients = [user.email])
    msg.body = f'''to reset your password, visit the following link
{url_for('users.reset_password',token = token, _external = True)}  
If you did not make this request, Ignore this mail
'''
    mail.send(msg)
#     mail.send_message('Password Reset Request',
#                       sender = os.environ.get('EMAIL_USER'),
#                       recipients=[user.email],
#                       body = f'''to reset your password, visit the following link
# {url_for('users.reset_password',token = token, _external = True)}  
# If you did not make this request, Ignore this mail
# ''')