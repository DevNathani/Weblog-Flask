# from flask import Blueprint
# import secrets
# import os
# from PIL import Image
from flask import render_template,url_for,flash,redirect,request,abort,Blueprint
from flask_blog.posts.forms import NewPost
from flask_blog.models import Posts
from flask_blog import db
# from flask_mail import Message
from flask_login import current_user,login_required

posts = Blueprint('posts',__name__)

@posts.route("/posts/new",methods = ['GET','POST'])
@login_required
def new():
    form = NewPost()
    if form.validate_on_submit():
        post = Posts(title = form.title.data, content = form.content.data, author = current_user)
        # with posts.app_context():
        db.session.add(post)
        db.session.commit()
        flash("Your Post had been added Successfully","success")
        return redirect(url_for("main.home"))
    return render_template('new_post.html',form = form, legend = 'New Post')

@posts.route("/posts/<int:post_id>")
def post(post_id):

    post = Posts.query.get_or_404(post_id)
    return render_template("post.html",post = post)


@posts.route("/posts/<int:post_id>/update",methods = ['GET','POST'])
@login_required
def update_post(post_id):
    post = Posts.query.get_or_404(post_id)

    if post.author != current_user:
        abort(403)
    form = NewPost()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data

        db.session.commit()
        flash("Your Post has been Updated Successfully!",'success')
        return redirect(url_for('posts.post',post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('new_post.html',form = form,legend = 'Update Post')

@posts.route("/posts/<int:post_id>/delete",methods = ['POST'])
@login_required
def delete_post(post_id):
    post = Posts.query.get_or_404(post_id)

    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Your Post has been Deleted Successfully!!",'success')
    return redirect(url_for('main.home'))


