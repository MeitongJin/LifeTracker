from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional

class PasswordResetForm(FlaskForm):
    csrf_token = HiddenField()  

    #get email
    email = StringField(
        'Email',
        validators=[Optional(), Email(message="Invalid email address.")]
    )

    #get code
    code = StringField(
        'Verification Code',
        validators=[Optional(), Length(min=4, max=10, message="Enter valid code.")]
    )

    #get passwords
    password = PasswordField(
        'New Password',
        validators=[Optional(), Length(min=6, message="Password must be at least 6 characters.")]
    )
    password_confirm = PasswordField(
        'Confirm Password',
        validators=[Optional(), EqualTo('password', message='Passwords must match.')]
    )

    submit = SubmitField('Submit')
