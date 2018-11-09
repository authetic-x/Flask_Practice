from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, SubmitField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Length, Regexp, Optional, ValidationError
from flask_login import current_user

from albumy.models import User


class EditProfileForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 30)])
    username = StringField('Username', validators=[DataRequired(), Length(1, 20),
                        Regexp('^[a-z0-9A-Z]*$', message='The username should contain only a-z, A-Z and 0-9')])
    website = StringField('Website', validators=[Optional(), Length(0, 254)])
    location = StringField('City', validators=[Optional(), Length(0, 50)])
    bio = TextAreaField('Bio', validators=[Optional(), Length(0, 120)])
    submit = SubmitField()

    def validate_username(self, filed):
        if filed.data != current_user.username and User.query.filter_by(username=filed.data).first():
            raise ValidationError('The username is already in use.')

class UploadAvatarForm(FlaskForm):
    image = FileField('Upload (<=3M)', validators=[FileRequired(), FileAllowed(['jpg','png'],
                                            'The file format should be .jpg or .png.')])
    submit = SubmitField()

class CropAvatarForm(FlaskForm):
    x = HiddenField()
    y = HiddenField()
    w = HiddenField()
    h = HiddenField()
    submit = SubmitField('Crop and Update')