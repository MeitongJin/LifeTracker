# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf.csrf import CSRFProtect
from datetime import datetime
from models import db, User
from input import input_bp
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Should be in environment variables in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lifetracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
csrf = CSRFProtect(app)

# Register Blueprint (/submit interface)
app.register_blueprint(input_bp)

# Create tables
with app.app_context():
    db.create_all()

# Helper functions
def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)

def validate_phone(phone):
    return len(phone) == 10 and phone.isdigit()

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['user_name'] = user.first_name
            flash("Login successful!", "success")
            return redirect(url_for('home'))
        else:
            flash("Invalid email or password", "error")
            return render_template('login.html')

    csrf_token = generate_csrf()
    return render_template('login.html', csrf_token=csrf_token)

# Home Route (after login)
@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('homepage.html', user_name=session.get('user_name'))

# Logout
@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))

# Register routes
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        errors = {}  #<-- Dictionary to store field-specific errors

        # Get form data with default empty strings
        first_name = request.form.get('firstname', '').strip()
        last_name = request.form.get('lastname', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()  # Added default empty string
        password = request.form.get('password', '')
        password_confirm = request.form.get('password_confirm', '')   

        # Validation
        if not first_name:
            errors['firstname'] = 'First name is required.'
        if not last_name:
            errors['lastname'] = 'Last name is required.'
        if not email:
            errors['email'] = 'Email is required.'
        elif not validate_email(email):
            errors['email'] = 'Invalid email format.'
        elif User.query.filter_by(email=email).first():
            errors['email'] = 'Email already registered.'
        if not phone:
            errors['phone'] = 'Phone number is required.'
        elif not validate_phone(phone):
            errors['phone'] = 'Phone number must be 10 digits.'
        if not password:
            errors['password'] = 'Password is required.'
        elif len(password) < 8:
            errors['password'] = 'Password must be at least 8 characters.'

        if password != password_confirm:
            errors['password_confirm'] = 'Passwords do not match.'

        # If any errors, re-render the form with them
        if errors:
            return render_template('register.html', errors=errors,
                                   firstname=first_name, lastname=last_name,
                                   email=email, phone=phone)

        # Create new user
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone
        )
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', errors={}, first_name='', last_name='', email='', phone='')

# When the user opens the website, it will automatically jump to the login page
@app.route('/')
def index():
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

    

