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
    username = StringField("Username", validators=[validators.DataRequired(message="Username is required")])
    password = PasswordField(
        "Password",
        validators=[
            validators.DataRequired(message="Password is required"),
            validators.Length(min=6, message="Min 6 length of password is required")
        ]
    )
    remember = BooleanField("Remember")
    submit = SubmitField("Log In")


class RegisterForm(LoginForm):
    """
    Register form
    """
    email = EmailField("Email", validators=[validators.DataRequired(message="Email is required"), validators.Email()])
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            validators.DataRequired(message="Confirm password is required"),
            validators.EqualTo("password", message="Passwords should match")
        ]
    )
    first_name = StringField("First Name", description='Optional')
    last_name = StringField("Last Name", description='Optional')
    facebook = StringField('Facebook', description='Optional')
    linkedin = StringField('LinkedIn', description='Optional')
    submit = SubmitField("Register")
