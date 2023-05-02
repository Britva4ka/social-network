import base64
from datetime import datetime
from hashlib import md5

from sqlalchemy.ext.hybrid import hybrid_property

from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import os
from PIL import Image
import io


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)


class User(BaseModel, UserMixin):
    __tablename__ = "user"

    username = db.Column(db.String, unique=True, index=True)
    email = db.Column(db.String, unique=True, index=True)
    password = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    avatar = db.Column(db.String(120), unique=True, nullable=True)

    posts = db.relationship(
        "Post", backref="author", uselist=True, lazy="dynamic", cascade="all,delete"
    )
    likes = db.relationship(
        'Like', backref='user', lazy='dynamic', primaryjoin='User.id==Like.user_id', cascade="all,delete"
    )
    dislikes = db.relationship(
        'Dislike', backref='user', lazy='dynamic', primaryjoin='User.id==Dislike.user_id', cascade="all,delete"
    )

    # list of users that follow you
    followers = db.relationship("Follow", backref="followee", foreign_keys="Follow.followee_id", cascade="all,delete")

    # list of users that you follow
    following = db.relationship("Follow", backref="follower", foreign_keys="Follow.follower_id", cascade="all,delete")

    message_sender = db.relationship(
        "Message", backref="sender", foreign_keys="Message.sender_id", cascade="all,delete")
    message_receiver = db.relationship(
        "Message", backref="receiver", foreign_keys="Message.receiver_id", cascade="all,delete")

    def set_avatar(self, size):
        if self.avatar:
            # return url_for('uploads', filename=f'{self.avatar}')
            from config import Config
            avatar_path = os.path.join(Config.UPLOADED_PHOTOS_DEST, self.avatar)  # chat_gpt :)
            with open(avatar_path, 'rb') as f:
                img = Image.open(io.BytesIO(f.read()))
                img.thumbnail((size, size))
                img_byte_arr = io.BytesIO()
                img.save(img_byte_arr, format='PNG')
                img_byte_arr = img_byte_arr.getvalue()
            return f"data:image/png;base64,{base64.b64encode(img_byte_arr).decode()}"
        else:
            digest = md5(self.email.lower().encode('utf-8')).hexdigest()
            return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'

    def set_password(self, password):
        """
        Set user password hash
        """
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """
        Check user password hash with existing in db
        """
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"{self.username}({self.email})"


class Profile(BaseModel):
    __tablename__ = "profiles"
    __table_args__ = (
        db.Index("idx_profiles_user_id", "user_id"),
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id", name="fk_profiles_user_id", ondelete="CASCADE"),
        nullable=False
    )
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    bio = db.Column(db.String)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    facebook = db.Column(db.String)
    linkedin = db.Column(db.String)

    user = db.relationship("User", backref=db.backref("profile", uselist=False), uselist=False)

    @hybrid_property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @full_name.expression
    def full_name(cls):
        return cls.first_name + ' ' + cls.last_name


class Post(BaseModel):
    __tablename__ = 'posts'

    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    author_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id", name="fk_posts_author_id", ondelete="CASCADE"),
        nullable=False
    )

    likes = db.relationship("Like", backref="post", uselist=True, cascade="all,delete")
    dislikes = db.relationship("Dislike", backref="post", uselist=True, cascade="all,delete")


# Like model
class Like(BaseModel):
    __tablename__ = "likes"

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id', name="fk_likes_user_id"),
        nullable=False
    )
    post_id = db.Column(
        db.Integer,
        db.ForeignKey('posts.id', name="fk_likes_post_id"),
        nullable=False
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# Dislike model
class Dislike(BaseModel):
    __tablename__ = "dislikes"
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id', name="fk_dislikes_user_id"),
        nullable=False
    )
    post_id = db.Column(
        db.Integer,
        db.ForeignKey('posts.id', name="fk_dislikes_post_id"),
        nullable=False
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Follow(db.Model):
    __tablename__ = 'follows'

    follower_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id', name="fk_follows_follower_id"),
        primary_key=True
    )
    followee_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id', name="fk_follows_followee_id"),
        primary_key=True
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Message(BaseModel):
    __tablename__ = 'messages'

    sender_id = db.Column(db.Integer, db.ForeignKey('user.id', name="fk_sender_id"), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id', name="fk_receiver_id"), nullable=False)
    content = db.Column(db.String(1000))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
