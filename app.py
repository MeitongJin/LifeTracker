# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf.csrf import CSRFProtect
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Should be in environment variables in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lifetracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
csrf = CSRFProtect(app)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Create tables
with app.app_context():
    db.create_all()

# Helper functions
def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)

def validate_phone(phone):
    return len(phone) == 10 and phone.isdigit()

# Routes
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form data
        first_name = request.form.get('firstname').strip()
        last_name = request.form.get('lastname').strip()
        email = request.form.get('email').strip()
        phone = request.form.get('phone').strip()
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')

        # Validation
        errors = []
        if not all([first_name, last_name, email, phone, password, password_confirm]):
            errors.append('All fields are required.')
        if not validate_email(email):
            errors.append('Invalid email format.')
        if not validate_phone(phone):
            errors.append('Phone number must be 10 digits.')
        if password != password_confirm:
            errors.append('Passwords do not match.')
        if len(password) < 8:
            errors.append('Password must be at least 8 characters.')
        if User.query.filter_by(email=email).first():
            errors.append('Email already registered.')

        if errors:
            for error in errors:
                flash(error, 'error')
            return redirect(url_for('register'))

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

    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
