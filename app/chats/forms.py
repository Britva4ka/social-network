from flask_wtf import FlaskForm
from wtforms import (
    TextAreaField,
    SubmitField,
    validators
)
# from wtforms.csrf.session import SessionCSRF


class ChatForm(FlaskForm):
    # class Meta:
    #     csrf = True
    #     csrf_class = SessionCSRF
    content = TextAreaField('Content', validators=[validators.DataRequired(message="You need print something"),
                                                   validators.Length(min=1, max=1000)])
    submit = SubmitField("Send")
