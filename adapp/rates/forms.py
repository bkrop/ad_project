from flask_wtf import FlaskForm
from wtforms import RadioField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class RateUserForm(FlaskForm):
    rate = RadioField('Rate user', validators=[DataRequired()], choices=[('thumb up', 'thumb up'), ('thumb down', 'thumb down')])
    comment = TextAreaField('Comment', validators=[Length(max=100)])
    submit = SubmitField('Confirm')