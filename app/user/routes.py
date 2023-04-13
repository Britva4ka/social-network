import os
from werkzeug.utils import secure_filename
from app import db
from app.models import User, Post, Follow
from app.post.forms import PostForm
from app.user import bp
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from flask_wtf.csrf import generate_csrf
from app.user.forms import ProfileForm
from config import Config
from datetime import datetime, timedelta


@bp.route("/blog")
@login_required
def blog():
    """
    Display user posts view
    """
    form = PostForm()
    posts = (
        db.session.query(Post)
        .filter(
            Post.author_id == current_user.id
        )
        .order_by(Post.created_at.desc())
        .all()
    )
    return render_template("user/blog.html", posts=posts, form=form)


@bp.route("/profile/<string:username>", methods=['GET', 'POST'])
@login_required
def profile(username):

    user = db.session.query(User).filter(User.username == username).first_or_404()

    if user.profile.last_seen > datetime.utcnow() - timedelta(minutes=5):
        status = 'Online'
    else:
        status = 'Last seen: ' + user.profile.last_seen.strftime('%Y-%m-%d %H:%M:%S')

    following = User.query.join(
        Follow, Follow.followee_id == User.id
    ).filter(
        Follow.follower_id == user.id
    ).all()

    followers = User.query.join(
        Follow, Follow.follower_id == User.id
    ).filter(
        Follow.followee_id == user.id
    ).all()

    form = ProfileForm()
    is_following = Follow.query.filter_by(follower_id=current_user.id, followee_id=user.id).first()
    csrf_token = generate_csrf()

    if form.validate_on_submit():

        user.profile.first_name = form.first_name.data
        user.profile.last_name = form.last_name.data
        user.profile.linkedin = form.linkedin.data
        user.profile.facebook = form.facebook.data
        user.profile.bio = form.bio.data
        filename = f"{user.username}_{user.id}_{secure_filename(form.photo.data.filename)}"
        if user.avatar:
            os.remove(os.path.join(Config.UPLOADED_PHOTOS_DEST, user.avatar))
        user.avatar = filename
        # form.photo.data.save(os.path.join(Config.UPLOADED_PHOTOS_DEST), filename)
        file_path = os.path.join(Config.UPLOADED_PHOTOS_DEST, filename)
        form.photo.data.save(file_path)

        # filename = photos.save(form.photo.data)
        # user.avatar = filename
        db.session.commit()
        flash('Your changes have been saved.', category="success")
        return redirect(url_for('user.profile', username=user.username))

    elif request.method == 'GET':
        form.first_name.data = user.profile.first_name
        form.last_name.data = user.profile.last_name
        form.linkedin.data = user.profile.linkedin
        form.facebook.data = user.profile.facebook
        form.bio.data = user.profile.bio
    return render_template('user/profile.html', user=user, form=form, is_following=is_following, csrf_token=csrf_token,
                           followers=followers, following=following, status=status)


@bp.route('/follow/<username>', methods=['GET', 'POST'])
@login_required
def follow(username):
    # follower_id = current_user.id
    followee = User.query.filter_by(username=username).first()
    # followee_id = followee.id
    if followee is None:
        flash('User {} not found.'.format(username), category="error")
        return redirect(url_for('index'))
    if followee == current_user:
        flash('You cannot follow yourself!', category="error")
        return redirect(url_for('user', username=username))
    follow = Follow(follower=current_user, followee=followee)
    db.session.add(follow)
    db.session.commit()
    flash('You are now following {}!'.format(username), category="success")
    return redirect(request.referrer)


@bp.route('/unfollow/<username>', methods=['GET', 'POST'])
@login_required
def unfollow(username):
    followee = User.query.filter_by(username=username).first()
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username), category="error")
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot unfollow yourself!', category="error")
        return redirect(url_for('user', username=username))
    follow = Follow.query.filter_by(follower=current_user, followee=followee).first()
    db.session.delete(follow)
    db.session.commit()
    flash('You are no longer following {}.'.format(username), category="success")
    return redirect(request.referrer)
