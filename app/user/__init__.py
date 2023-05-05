from pathlib import Path

import pandas as pd
from config import Config
from flask import Blueprint
from sqlalchemy import func # noqa
from .. import db
from ..models import Post, User, Profile # noqa

bp = Blueprint('user', __name__, url_prefix='/user')

from . import routes # noqa


@bp.cli.command("extract_users")
def extract_users():
    # users_info = db.session.query(
    #     User.username,
    #     User.email,
    #     Profile.full_name,
    #     func.count('*')
    # ).join(
    #     Profile, User.id == Profile.user_id).join(
    #     Post, User.id == Post.author_id
    # ).group_by(User.username, User.email, Profile.full_name).all()
    # print(*users_info, sep='\n')

    # Code upper is alternative for code below.

    users = db.session.query(User).all()
    users_info = [(user.username, user.email, user.profile.full_name, user.posts.count()) for user in users]
    users_info = sorted(users_info)
    # code below is constant
    df = pd.DataFrame(users_info, columns=['username', 'email', 'full_name', 'post_count'])
    Path(Config.CSV_DATA_DEST).mkdir(parents=True, exist_ok=True)
    df.to_csv(Config.CSV_DATA_DEST+"users_info.csv")
