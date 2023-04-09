# from app import db
from app.main import bp
from flask import render_template

# from app.models import Post


@bp.route("/")
@bp.route("/index")
def index():
    """
    View function to render home page of the 'Social Network' website
    :return:
    """
    # posts = db.session.query(Post).order_by(Post.created_at.desc()).all()
    posts = 'lol'

    # call special function to render template with passed context
    return render_template("index.html", posts=posts)


@bp.route("/about")
def about():
    context = {
        "title": "ABOUT US",
        "text": "blablabla"
    }
    return render_template('about.html', **context)
