from app.main import bp
from flask import render_template


@bp.route("/")
@bp.route("/index")
def index():
    """
    View function to render home page of the 'Social Network' website
    :return:
    """

    # sample template context to render
    context = {
        "user": {"username": "akushyn"},
        "title": "Hillel"
    }

    # call special function to render template with passed context
    return render_template("index.html", **context)


@bp.route("/about")
def about():
    context = {
        "title": "ABOUT US",
        "text": "blablabla"
    }
    return render_template('about.html', **context)

