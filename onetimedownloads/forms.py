from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(Form):
        email = StringField('name', validators=[DataRequired()])
        password = PasswordField('password', validators=[DataRequired()])
        submit = SubmitField()
