from app import db
from app.models import User, Profile, Post, Like, Dislike
from app.schemas import UserSchema, PostSchema


class UserService:

    def get_by_id(self, user_id):
        user = db.session.query(User).filter(User.id == user_id).first_or_404()
        return user

    def get_by_username(self, username):
        user = db.session.query(User).filter(User.username == username).first_or_404()
        return user

    def create(self, **kwargs):
        user = User(username=kwargs.get('username'), email=kwargs.get('email'))
        user.set_password(kwargs.get('password'))

        db.session.add(user)
        db.session.commit()

        profile = Profile(user_id=user.id)
        db.session.add(profile)
        db.session.commit()

        return user

    def update(self, data: dict):
        user = self.get_by_id(data['id'])
        data['profile']['id'] = user.profile.id
        data['profile']['user_id'] = user.id

        user = UserSchema(exclude=('password', 'last_seen', 'created_ad',)).load(data)
        db.session.add(user)
        db.session.commit()

        return user

    def delete(self, user_id):
        user = self.get_by_id(user_id)
        profile = user.profile
        db.session.delete(profile)
        db.session.commit()

        db.session.delete(user)
        db.session.commit()

        return True


class PostService:
    def create(self, **kwargs):
        post = Post(title=kwargs.get("title"), content=kwargs.get("content"), author_id=kwargs.get("author_id"))
        db.session.add(post)
        db.session.commit()
        return post

    def get_by_id(self, post_id):
        post = db.session.query(Post).filter(Post.id == post_id).first_or_404()
        return post

    def get_by_user_id(self, user_id):
        post = db.session.query(Post).filter(Post.author_id == user_id).first_or_404()
        return post

    def update(self, data: dict):
        post = self.get_by_id(data['id'])
        data['author_id'] = post.author_id
        post = PostSchema(only=('author_id', 'content', 'id', 'title',)).load(data)
        db.session.add(post)
        db.session.commit()

        return post

    def delete(self, post_id):
        post = self.get_by_id(post_id)
        likes = db.session.query(Like).filter_by(post_id=post_id).all()
        for like in likes:
            db.session.delete(like)
            db.session.commit()
        dislikes = db.session.query(Dislike).filter_by(post_id=post_id).all()
        for dislike in dislikes:
            db.session.delete(dislike)
            db.session.commit()
        db.session.delete(post)
        db.session.commit()

        return True
