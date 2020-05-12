from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import Length

class CreateMessageForm(FlaskForm):
    content = TextAreaField('Content', validators=[Length(min=1, max=300)])
    submit = SubmitField('Send')