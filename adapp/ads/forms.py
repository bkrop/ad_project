from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import Length, DataRequired

class CreatingAdForm(FlaskForm):
    title = StringField('Title', validators=[Length(min=5, max=100), DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired(), Length(min=5, max=300)])
    reward = StringField('Reward', validators=[DataRequired(), Length(min=1, max=100)])
    submit = SubmitField('Confirm')

class PickUserForm(FlaskForm):
    submit = SubmitField('Pick for this ad')

class FinishAdForm(FlaskForm):
    submit = SubmitField('Finish ad!')