from flask_restful import Resource
from flask import jsonify, request
from sqlalchemy.exc import IntegrityError

from app import db
from app.models import User, Profile, Post, Like, Dislike, Message
from app.schemas import UserSchema, ProfileSchema, PostSchema, LikeSchema, DislikeSchema, MessageSchema
from app.services import UserService, PostService

user_service = UserService()
post_service = PostService()


class UsersResource(Resource):
    def get(self):

        ordered = request.args.get('ordered', type=bool)

        users_query = db.session.query(User)
        if ordered:
            users_query = users_query.order_by(User.created_at.asc())

        users = users_query.all()
        return jsonify(UserSchema().dump(users, many=True))

    def post(self):
        json_data = request.get_json()
        if 'avatar' in json_data:
            response = jsonify({'error': 'avatar field not allowed'})
            response.status_code = 400
            return response
        else:
            #  Below was my experiment. I decided not delete it, because it works
            try:
                user = user_service.create(**json_data)
            except IntegrityError:
                response = jsonify({'error': 'User already exists'})
                response.status_code = 400
                return response
            else:
                response = jsonify(UserSchema().dump(user, many=False))
                response.status_code = 201
                return response


class UserResource(Resource):
    def get(self, user_id=None):
        user = user_service.get_by_id(user_id)
        return jsonify(UserSchema().dump(user, many=False))

    def put(self, user_id):
        json_data = request.get_json()
        json_data['id'] = user_id

        user = user_service.update(json_data)
        return jsonify(UserSchema().dump(user, many=False))

    def delete(self, user_id):
        status = user_service.delete(user_id)
        return jsonify(status=status)


class ProfilesResource(Resource):
    def get(self):
        profiles = db.session.query(Profile).all()
        return jsonify(ProfileSchema().dump(profiles, many=True))
    # no post method because profile creating automatic after creating user


class ProfileResource(Resource):
    def get(self, profile_id):
        profile = db.session.query(Profile).filter_by(user_id=profile_id).first_or_404()
        return jsonify(ProfileSchema().dump(profile, many=False))

    def put(self, profile_id):
        json_data = request.get_json()
        json_data['id'] = profile_id
        profile = db.session.query(Profile).filter(Profile.id == profile_id).first_or_404()
        json_data['user_id'] = profile.user_id
        profile = ProfileSchema().load(json_data)
        db.session.add(profile)
        db.session.commit()
        return jsonify(ProfileSchema().dump(profile, many=False))

    # no delete method, because user must have profile


class PostsResource(Resource):
    def get(self):
        posts = db.session.query(Post).all()
        return jsonify(PostSchema().dump(posts, many=True))

    def post(self):
        json_data = request.get_json()
        post = post_service.create(**json_data)
        response = jsonify(PostSchema().dump(post, many=False))
        response.status_code = 201
        return response


class PostResource(Resource):
    def get(self, post_id=None):
        post = post_service.get_by_id(post_id)
        return jsonify(PostSchema().dump(post, many=False))

    def put(self, post_id):
        json_data = request.get_json()
        json_data['id'] = post_id

        post = post_service.update(json_data)
        return jsonify(PostSchema().dump(post, many=False))

    def delete(self, post_id):
        status = post_service.delete(post_id)
        return jsonify(status=status)


class UsersPostsResource(Resource):
    def get(self, user_id):
        posts = db.session.query(Post).filter_by(author_id=user_id). all()
        return jsonify(PostSchema().dump(posts, many=True))

    def post(self, user_id):
        json_data = request.get_json()
        json_data['author_id'] = user_id
        post = post_service.create(**json_data)
        response = jsonify(PostSchema().dump(post, many=False))
        response.status_code = 201
        return response


class UsersPostResource(Resource):
    def get(self, user_id, post_id):
        post = db.session.query(Post).filter_by(author_id=user_id, id=post_id).first_or_404()
        return jsonify(PostSchema().dump(post, many=False))

    def post(self, user_id, post_id):
        json_data = request.get_json()
        json_data['author_id'] = user_id
        json_data['id'] = post_id
        post = post_service.create(**json_data)
        response = jsonify(PostSchema().dump(post, many=False))
        response.status_code = 201
        return response

    def put(self, user_id, post_id):
        json_data = request.get_json()
        json_data['id'] = post_id
        json_data['author_id'] = user_id

        post = post_service.update(json_data)
        return jsonify(PostSchema().dump(post, many=False))

    def delete(self, user_id, post_id):
        post = db.session.query(Post).filter_by(author_id=user_id, id=post_id).first_or_404()
        status = post_service.delete(post.id)
        return status


class LikesResource(Resource):
    def get(self):
        likes = db.session.query(Like).all()
        return jsonify(LikeSchema().dump(likes, many=True))

    def post(self):
        json_data = request.get_json()
        check = db.session.query(Like).filter(Like.post_id == json_data.get("post_id"),
                                              Like.user_id == json_data.get("user_id")).first()
        if not check:
            like = Like(user_id=json_data.get("user_id"), post_id=json_data.get("post_id"))
            db.session.add(like)
            db.session.commit()
            response = jsonify(LikeSchema().dump(like, many=False))
            response.status_code = 201
            return response
        else:
            return "Error, this like is already exist"


class LikeResource(Resource):
    def get(self, like_id):
        like = db.session.query(Like).filter(Like.id == like_id).first_or_404()
        return jsonify(LikeSchema().dump(like, many=False))

    # no put method because there are nothing to change in likes
    def delete(self, like_id):
        like = db.session.query(Like).filter(Like.id == like_id).first_or_404()
        db.session.delete(like)
        db.session.commit()
        return True


class DisLikesResource(Resource):
    def get(self):
        dislikes = db.session.query(Dislike).all()
        return jsonify(DislikeSchema().dump(dislikes, many=True))

    def post(self):
        json_data = request.get_json()
        check = db.session.query(Dislike).filter(Dislike.post_id == json_data.get("post_id"),
                                                 Dislike.user_id == json_data.get("user_id")).first()
        if not check:
            dislike = Dislike(user_id=json_data.get("user_id"), post_id=json_data.get("post_id"))
            db.session.add(dislike)
            db.session.commit()
            response = jsonify(DislikeSchema().dump(dislike, many=False))
            response.status_code = 201
            return response
        else:
            return "Error, this dislike is already exist"


class DisLikeResource(Resource):
    def get(self, dislike_id):
        dislike = db.session.query(Dislike).filter(Dislike.id == dislike_id).first_or_404()
        return jsonify(DislikeSchema().dump(dislike, many=False))

    # no put method because there are nothing to change in dislikes
    def delete(self, dislike_id):
        dislike = db.session.query(Dislike).filter(Dislike.id == dislike_id).first_or_404()
        db.session.delete(dislike)
        db.session.commit()
        return True


class MessagesResource(Resource):
    def get(self):
        messages = db.session.query(Message).all()
        return jsonify(MessageSchema().dump(messages, many=True))

    def post(self):
        json_data = request.get_json()
        message = Message(sender_id=json_data['sender_id'], receiver_id=json_data['receiver_id'],
                          content=json_data['content'])
        db.session.add(message)
        db.session.commit()
        response = jsonify(MessageSchema().dump(message, many=False))
        response.status_code = 201
        return response


class MessageResource(Resource):
    def get(self, message_id):
        message = db.session.query(Message).filter(Message.id == message_id).first_or_404()
        return jsonify(MessageSchema().dump(message, many=False))

    def put(self, message_id):
        json_data = request.get_json()
        json_data['id'] = message_id
        message = db.session.query(Message).filter(Message.id == message_id).first_or_404()
        json_data['sender_id'] = message.sender_id
        json_data['receiver_id'] = message.receiver_id
        message = MessageSchema().load(json_data)
        db.session.add(message)
        db.session.commit()
        return jsonify(MessageSchema().dump(message, many=False))

    def delete(self, message_id):
        message = db.session.query(Message).filter(Message.id == message_id).first_or_404()
        db.session.delete(message)
        db.session.commit()
        return True
