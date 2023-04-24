from flask import Blueprint
from flask_restful import Api
from .resources import UsersResource, UserResource, ProfilesResource, ProfileResource, \
    PostsResource, LikesResource, DisLikesResource, PostResource, UsersPostsResource, UsersPostResource, \
    LikeResource, DisLikeResource, MessagesResource, MessageResource

bp = Blueprint('api', __name__, url_prefix="/api")
api = Api(bp)

api.add_resource(UsersResource, '/users', endpoint="users_list")
api.add_resource(UserResource, '/users/<int:user_id>', endpoint="users_details")
api.add_resource(ProfilesResource, '/profiles', endpoint="profiles_list")
api.add_resource(ProfileResource, '/profiles/<int:profile_id>', endpoint="profile_details")
api.add_resource(PostsResource, '/posts', endpoint="posts_list")
api.add_resource(PostResource, '/posts/<int:post_id>', endpoint="post_details")
api.add_resource(UsersPostsResource, '/users/<int:user_id>/posts', endpoint="users_posts_list")
api.add_resource(UsersPostResource, '/users/<int:user_id>/posts/<int:post_id>', endpoint="users_post_details")
api.add_resource(LikesResource, '/likes', endpoint="likes_list")
api.add_resource(DisLikesResource, '/dislikes', endpoint="dislikes_list")
api.add_resource(LikeResource, '/likes/<int:like_id>', endpoint="like_details")
api.add_resource(DisLikeResource, '/dislikes/<int:dislike_id>', endpoint="dislike_details")
api.add_resource(MessagesResource, '/messages', endpoint="messages_list")
api.add_resource(MessageResource, '/messages/<int:message_id>', endpoint="message_details")
