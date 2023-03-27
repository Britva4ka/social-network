from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    SubmitField,
    EmailField,
    validators
)


class LoginForm(FlaskForm):
    """
    Login form
    """
    username = StringField("Username", validators=[validators.DataRequired()])
    password = PasswordField("Password", validators=[validators.DataRequired()])
    remember = BooleanField("Remember")
    submit = SubmitField("Log In")


class RegisterForm(LoginForm):
    """
    Register form
    """
    email = EmailField("E-mail", validators=[validators.DataRequired(), validators.Email()])
    submit = SubmitField("Register")