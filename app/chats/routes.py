from flask import render_template, redirect, request, flash

from app import db
from app.models import User, Message
from app.chats import bp
from flask_login import current_user, login_required
from app.chats.forms import ChatForm


@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    # hardcode time :)
    messages = db.session.query(Message).filter(
        (Message.sender_id == current_user.id) | (Message.receiver_id == current_user.id)
    ).order_by(Message.created_at.desc()).all()
    chats = []
    for message in messages:
        if message.sender_id in chats or message.receiver_id in chats:
            continue
        if message.sender_id != current_user.id:
            chats.append(message.sender_id)
        elif message.receiver_id != current_user.id:
            chats.append(message.receiver_id)
    users = []
    for user_id in chats:
        user = db.session.query(User).filter(User.id == user_id).first()
        users.append(user)
    return render_template("chats/dialogues.html", users=users)


@bp.route("/chat/<string:username>", methods=['GET', 'POST'])
@login_required
def chat(username):
    user = db.session.query(User).filter(User.username == username).first_or_404()
    if user is None:
        flash(f'User {username} not found.', category="error")
        return redirect(request.referrer)
    if user == current_user:
        flash('You cannot chat with yourself!', category="error")
        return redirect(request.referrer)
    form = ChatForm()
    messages = (
        db.session.query(Message)
        .filter(
            (Message.sender_id == current_user.id) | (Message.receiver_id == current_user.id),
            (Message.sender_id == user.id) | (Message.receiver_id == user.id)
        )
        .order_by(Message.created_at.desc())
        .all()
    )
    if form.validate_on_submit():
        message = Message(sender_id=current_user.id, receiver_id=user.id, content=form.content.data)
        db.session.add(message)
        db.session.commit()
        flash("You sent a message.", category='success')
        return redirect(request.referrer)

    return render_template("chats/chat.html", messages=messages, form=form, user=user)
