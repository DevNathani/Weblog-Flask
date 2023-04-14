# from datetime import datetime
import jwt
import datetime
# from itsdangerous import URLSafeSerializer as Serializer
from flask_blog import db,login_manager
from flask import current_app
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model,UserMixin):
    id = db.Column(db.Integer(),primary_key = True)
    username = db.Column(db.String(20), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    image_file = db.Column(db.String(20),default = 'default.jpg', nullable = False)
    password = db.Column(db.String(60),nullable = False)

    posts = db.relationship('Posts',backref = 'author',lazy = True)

    # this deals with how object will look when called 
    def __repl__(self):
        return f"{self.username}, {self.email}, {self.image_file}"
    
    def get_reset_token(self,expiry_sec = 1800):    
        reset_token = jwt.encode(
        {
            "user_id": self.id,
            "exp": datetime.datetime.now(tz=datetime.timezone.utc)
                    + datetime.timedelta(seconds=expiry_sec)
        },
        current_app.config['SECRET_KEY'],
        algorithm="HS256"
        )
        return reset_token

    @staticmethod
    def verify_token(token):
        try:
            data = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                leeway=datetime.timedelta(seconds=10),
                algorithms=["HS256"]
            )
            user_id = data.get('user_id')
        except:
            return None
        
        return User.query.get(user_id)

class Posts(db.Model):
    id = db.Column(db.Integer(),primary_key = True)
    title = db.Column(db.String(120), nullable = False)
    content = db.Column(db.Text,nullable = False)
    date_posted = db.Column(db.DateTime,nullable = False,default = datetime.datetime.utcnow)
    user_id = db.Column(db.Integer(),db.ForeignKey('user.id'),nullable = True)

    def __repl__(self):
        return f"{self.title}, {self.date_posted}"


class Contacts(db.Model):
    id = db.Column(db.Integer(),primary_key = True)
    email = db.Column(db.String(120), nullable = False,unique = True)
    subject = db.Column(db.String(120), nullable = False)
    content = db.Column(db.Text,nullable = False)
    date_posted = db.Column(db.DateTime,nullable = False,default = datetime.datetime.utcnow)

    def __repl__(self):
        return f"{self.title}, {self.date_posted}"
