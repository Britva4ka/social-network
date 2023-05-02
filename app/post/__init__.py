import click
import pandas as pd
from flask import Blueprint
from sqlalchemy import func # noqa

from config import Config
from .. import db
from ..models import Post, Like, Dislike, User # noqa

bp = Blueprint('post', __name__, url_prefix='/post')

from . import routes  # noqa


@bp.cli.command("extract_posts")
@click.argument('user_id', type=int)
def extract_posts(user_id):
    user = db.session.query(User).filter(User.id == user_id).first_or_404()
    # code upper is constant

    # post_info = db.session.query(
    #     Post.title, func.count(Like.id), func.count(Dislike.id), Post.created_at
    # ).outerjoin(
    #     Like,
    #     Post.id == Like.post_id
    # ).outerjoin(
    #     Dislike, Post.id == Dislike.post_id
    # ).group_by(Post.title, Post.created_at).filter(
    #     Post.author_id == user_id
    # ).order_by(
    #     Post.created_at
    # ).all()
    # print(*post_info, sep='\n')

    # Code upper is alternative for code below.

    post_info = [(post.title, len(post.likes), len(post.dislikes), post.created_at) for post in user.posts]
    post_info = sorted(post_info, key=lambda x: x[-1])
    # code below is constant
    df = pd.DataFrame(post_info, columns=['title', 'likes', 'dislikes', 'created_at'])
    df.to_csv(Config.CSV_DATA_DEST+f"{user.username}_posts.csv")
