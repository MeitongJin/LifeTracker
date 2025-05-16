from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, TelField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp

class RegisterForm(FlaskForm):
    firstname = StringField('First Name', validators=[
        DataRequired(message="First name is required."),
        Length(min=2, max=50)
    ])
    
    lastname = StringField('Last Name', validators=[
        DataRequired(message="Last name is required."),
        Length(min=2, max=50)
    ])
    
    email = EmailField('Email', validators=[
        DataRequired(message="Email is required."),
        Email(message="Invalid email format.")
    ])
    
    phone = TelField('Phone Number', validators=[
        DataRequired(message="Phone number is required."),
        Regexp(r'^\d{10}$', message="Phone number must be 10 digits.")
    ])
    
    password = PasswordField('Password', validators=[
        DataRequired(message="Password is required."),
        Length(min=6, message="Password must be at least 6 characters.")
    ])
    
    password_confirm = PasswordField('Confirm Password', validators=[
        DataRequired(message="Please confirm your password."),
        EqualTo('password', message="Passwords must match.")
    ])
    
    submit = SubmitField('Register')
