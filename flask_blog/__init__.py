# This Module contains all the modules required for the creation and the initialization of the application objects

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_blog.config import Config


# creating an instance of the Database
db = SQLAlchemy()

# creating an instance of bcrypt for hashing passwords
bcrypt = Bcrypt()

# creating an instance of LoginMAnager for managing Sessions of Logined USers
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

# creating and initializing variables to send mails for forgot password

mail = Mail()



def create_app(config_class = Config):
    
    app = Flask(__name__)
    app.config.from_object(Config)

    login_manager.init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)

    from flask_blog.users.routes import users
    from flask_blog.posts.routes import posts
    from flask_blog.main.routes import main
    from flask_blog.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app

