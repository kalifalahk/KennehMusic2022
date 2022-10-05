from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,TextAreaField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    name = StringField('Artist Name', validators=[DataRequired()])
    home = StringField('Hometown', validators=[DataRequired()])
    description = TextAreaField('Description')
    submit = SubmitField('Create New Artist')







