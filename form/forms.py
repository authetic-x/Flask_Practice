from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileAllowed, FileRequired

class LoginForm(FlaskForm):

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(),
                                                     Length(8, 128)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log in')

class UploadForm(FlaskForm):
    photo = FileField('Upload Image', validators=[FileRequired(),
                                        FileAllowed(['jpg','jpeg','png','gif'])])
    submit = SubmitField()