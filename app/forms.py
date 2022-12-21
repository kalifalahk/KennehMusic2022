from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, SelectMultipleField, DateField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User

class ArtistForm(FlaskForm):
    name = StringField('Artist Name', validators=[DataRequired()])
    home = StringField('Hometown', validators=[DataRequired()])
    description = TextAreaField('Description')
    submit = SubmitField('Create New Artist')

class VenueForm(FlaskForm):
    name = StringField('Venue Name', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State (2 letters e.g., NY, CA)', validators=[DataRequired()])
    submit = SubmitField('Create New Venue')

class EventForm(FlaskForm):
    name = StringField('Event Name', validators=[DataRequired()])
    date= DateField('Start Date', validators=[DataRequired()])
    venue = SelectField('Venue')
    artist = SelectMultipleField('Artists')
    submit = SubmitField('New Event')



class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')







