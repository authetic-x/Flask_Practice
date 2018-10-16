from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, MultipleFileField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_ckeditor import CKEditorField

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

class MultiUploadForm(FlaskForm):
    photo = MultipleFileField('Upload Image', validators={DataRequired()})
    submit = SubmitField()

class RichTextForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(1, 50)])
    body = CKEditorField('Body', validators=[DataRequired()])
    save = SubmitField('Save')
    publish = SubmitField('Publish')

class SigninForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1,20)])
    password = PasswordField('Password', ValueError=[DataRequired(), Length(8, 128)])
    submit1 = SubmitField('Sign in')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(8 ,128)])
    email = StringField('Email', validators=[DataRequired(), Length(1, 254)])
    submit2 = SubmitField('Register')