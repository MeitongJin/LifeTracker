from flask_wtf import FlaskForm
from wtforms import FloatField, IntegerField, RadioField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Optional

class DailyInputForm(FlaskForm):
    exercise = RadioField(
        'Did you exercise?',
        choices=[('yes', 'Yes'), ('no', 'No')],
        validators=[DataRequired()]
    )
    
    exercise_hours = FloatField(
        'Exercise Hours',
        validators=[Optional(), NumberRange(min=0, max=24)],
        default=0
    )
    
    water_intake = FloatField(
        'Water Intake (L)',
        validators=[DataRequired(), NumberRange(min=0, max=20)],
        default=0
    )
    
    sleep_hours = FloatField(
        'Sleep Hours',
        validators=[DataRequired(), NumberRange(min=0, max=24)],
        default=0
    )
    
    reading_hours = FloatField(
        'Reading Hours',
        validators=[DataRequired(), NumberRange(min=0, max=24)],
        default=0
    )
    
    meals = IntegerField(
        'Number of Meals',
        validators=[DataRequired(), NumberRange(min=0, max=10)],
        default=0
    )
    
    screen_hours = FloatField(
        'Screen Hours',
        validators=[DataRequired(), NumberRange(min=0, max=24)],
        default=0
    )
    
    productivity = SelectField(
        'Productivity Level',
        choices=[(str(i), str(i)) for i in range(1, 11)],
        validators=[DataRequired()]
    )
    
    mood = RadioField(
        'Mood',
        choices=[
            ('happy', 'Happy'),
            ('neutral', 'Neutral'),
            ('sad', 'Sad'),
            ('angry', 'Angry')
        ],
        validators=[DataRequired()]
    )
    
    submit = SubmitField('Submit')