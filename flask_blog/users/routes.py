from flask import Blueprint,render_template,url_for,flash,redirect,request
from flask_blog.users.forms import RegistrationForm,LoginForm,AccountUpdateForm,RequestResetForm,ResetPassword
from flask_blog.models import User,Posts
from flask_blog import db, bcrypt
from flask_login import login_user,current_user,logout_user,login_required
from flask_blog.users.utils import send_reset_email,save_picture

users = Blueprint('users',__name__)


@users.route("/register",methods = ['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # hashing passwords
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        #Inserting Data to site.db
        user = User(username = form.username.data, email = form.email.data, password = hashed_password)   
        # with users.app_context():
        db.session.add(user)
        db.session.commit()

        flash(f'The Account has been Created Successfully!!, You can now Login',category='success')
        return redirect(url_for('users.login'))
    return render_template('register.html',title = 'Register',form = form)


@users.route("/login", methods = ['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        
        if user and bcrypt.check_password_hash(user.password,form.password.data):
        # if form.username.data == 'admin' and form.password.data == 'password':
            login_user(user,remember = form.remember.data)
            next_page = request.args.get('next')
            flash('You are Successfully Logged In!',category='success')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('main.home')) 
        else:
            flash('Login Unsuccessful, Please Check the Username and Password','danger')   
    return render_template('login.html',title = 'Login',form = form)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/account",methods = ['GET','POST'])
@login_required
def account():
    form = AccountUpdateForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture = save_picture(form.picture.data)
            current_user.image_file = picture
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash(f"Your Account has been Updated Successfully","success")
        return redirect(url_for("users.account"))
    # elif request.method == 'GET':
        # form.username.data = current_user.username
        # form.email.data = current_user.email
    image_file = url_for('static', filename = f'profile_pics/{current_user.image_file}')
    return render_template('account.html',title = 'Account',image_file = image_file,form = form,user = current_user)


@users.route("/user/<string:username>")
def user_post(username):
    page = request.args.get('page',1,type = int)
    user = User.query.filter_by(username = username).first_or_404()
    posts = Posts.query.filter_by(author = user).\
            order_by(Posts.date_posted.desc()).\
            paginate(page = page,per_page = 4)
    return render_template('user_post.html',posts = posts,user = user)


@users.route("/reset_password",methods = ['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        send_reset_email(user)
        flash("A Confirmation Email has been sent to you, Please confirm to continue",'info')
        return redirect(url_for('users.login'))
    return render_template("reset_request.html",form = form)

@users.route("/reset_password/<string:token>",methods = ['GET','POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_token(token)
    if user is None:
        flash("Time Limit Exceeded",'warning')
        return render_template(url_for('users.reset_request'))
    form = ResetPassword()
    if form.validate_on_submit():
    # hashing passwords
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        #changing Password in the Database
        user.password = hashed_password
        db.session.commit()

        flash(f'Your Password has been Successfully Updated',category='success')
        return redirect(url_for('users.login'))
    return render_template("reset_password.html",form = form)