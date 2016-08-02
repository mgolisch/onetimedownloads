from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired


class LoginForm(Form):
        email = StringField('name', validators=[DataRequired()])
        password = PasswordField('password', validators=[DataRequired()])
        submit = SubmitField()

class UploadForm(Form):
        file = FileField('file')
        submit = SubmitField()

class DownloadForm(Form):
        code = StringField('code',validators=[DataRequired()])
        submit = SubmitField()

    