
from flask import render_template, url_for, redirect, request, flash, abort
from flask_login import current_user, login_required

from app import app
from app import db
from app.main import main
from app.main.forms import UpdateAccountForm, PostForm
from app.models import Post, Clap, Comment
from app.requests import getQuotes


@main.route('/')
def index():
    quotes = getQuotes()
    posts = Post.query.all()
    return render_template("index.html", posts=posts, quotes=quotes,  current_user=current_user)


@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'Thank you')
        return redirect(url_for('main.profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pic/' + current_user.image_file)
    return render_template('profile/profile.html', title='Profile', image_file=image_file, form=form)


@main.route("/new_post", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,sub_title = form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        
        flash('Your post was successfully generated!', 'Thank you')
        return redirect(url_for('main.index'))
    return render_template('new_post.html', title='New Post',form=form, legend='New Post')


@main.route("/post/<int:post_id>")
@login_required
def mypost(post_id):
    comments = Comment.query.filter_by(post_id=post_id).all()
    print(comments)
    heading = 'comments'
    post = Post.query.get_or_404(post_id)
    return render_template('posts.html', title=post.title, post=post, comments=comments, heading=heading)


@main.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('main.my_post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('new_post.html', title='Update Post',form=form, legend='Update Post')

@main.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    post.delete()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.index'))

@main.route('/like/<int:id>', methods=['POST', 'GET'])
@login_required
def upvote(id):
    post = Post.query.get(id)
    clap = Clap(post=post, upvote=1)
    clap.save()
    return redirect(url_for('main.my_posts'))


@main.route('/comment/<post_id>', methods=['Post', 'GET'])
@login_required
def comment(post_id):
    comment = request.form.get('newcomment')
    new_comment = Comment(comment=comment,user_id=current_user._get_current_object().id, post_id=post_id)
    new_comment.save()
    return redirect(url_for('main.my_post',post_id=post_id))




