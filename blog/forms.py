from flask_wtf import FlaskForm
from wtforms import  StringField, PasswordField, validators


class RegistrationForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=4, max=25), validators.DataRequired()])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match'),
        validators.Length(min=8, max=25)
    ])
    confirm = PasswordField('Repeat Password', [validators.DataRequired()])


class LoginForm(FlaskForm):
    username = StringField('Username', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])

class BlogEntry(FlaskForm):
    title = StringField('title', [validators.DataRequired()])
    body = StringField('body', [validators.DataRequired()])