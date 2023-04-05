
from flask_login import current_user
from flask import render_template,request,Blueprint,redirect,url_for,flash
from flask_blog.models import Posts
from flask_blog.main.forms import Contact
from flask_blog.models import Contacts
from flask_blog import db
from flask_blog.main.utils import send_feedback_email

main = Blueprint('main',__name__)


@main.route("/")
def home():

    page = request.args.get('page',1,type = int)
    posts = Posts.query.order_by(Posts.date_posted.desc()).paginate(page = page,per_page = 4)
    return render_template('index.html',posts = posts)

@main.route("/about")
def about():
    return render_template('about.html')

@main.route("/contact",methods = ['GET','POST'])
def contact():
    form = Contact()
    if current_user.is_authenticated:
        form.email.data = current_user.email
    if form.validate_on_submit():
        send_feedback_email(form)
        feed = Contacts(email = form.email.data, subject = form.subject.data, content = form.description.data)   
        # with users.app_context():
        db.session.add(feed)
        db.session.commit()
        flash(f'Message Successfully Sent, We will respond you ASAP through the email you have provided','success')
        return redirect(url_for('main.home'))
    return render_template('contact.html',form = form)