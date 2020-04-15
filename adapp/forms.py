from adapp.models import User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextField
from wtforms.validators import Email, equal_to, DataRequired, Length, ValidationError

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=5, max=100)])
    name = StringField('Name', validators=[Length(min=3, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=60)])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), equal_to('password')])
    submit = SubmitField('Register')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is taken')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
    remember = BooleanField('Remember me')

class CreatingAdForm(FlaskForm):
    title = StringField('Title', validators=[Length(min=5, max=100), DataRequired()])
    content = TextField('Content', validators=[DataRequired(), Length(min=5, max=300)])
    submit = SubmitField('Create')