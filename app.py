from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_migrate import Migrate # Import Migrate
from flask_wtf.csrf import generate_csrf
import re
from random import randint
from flask_mail import Mail, Message
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
# Custom modules
from extensions import db, csrf
from models import User, UserInput
from input import to_float, to_int
from output import get_past_week_inputs, generate_bar_chart, generate_pie_chart

app = Flask(__name__)

# Email configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'team.lifetracker@gmail.com'  
app.config['MAIL_PASSWORD'] = 'otre nlsm fdcj josn'
app.config['MAIL_DEFAULT_SENDER'] = 'team.lifetracker@gmail.com'  

mail = Mail(app)

app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lifetracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)

def validate_phone(phone):
    return len(phone) == 10 and phone.isdigit()

def send_reset_email(email, code):
    try:
        msg = Message(
            "Your Password Reset Code",
            sender=app.config['MAIL_DEFAULT_SENDER'],
            recipients=[email]
        )
        msg.body = f"""Your password reset code is: {code}
        
This code will expire in 10 minutes."""
        mail.send(msg)
        print(f"Email sent to {email}")  # Debug output
        return True
    except Exception as e:
        print(f"Failed to send email: {str(e)}")  # Detailed error logging
        return False
    
# Initialize extensions
db.init_app(app)
csrf.init_app(app)
migrate = Migrate(app, db) # Update the database with Flask-Migrate

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

# Register Route
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

# Reset Password
@app.route('/resetPassword', methods=['GET', 'POST'])
def reset_password():
    # Always generate CSRF token
    csrf_token = generate_csrf()
    
    # Handle forced reset or resend requests
    if request.args.get('force') == '1':
        session.pop('reset_email', None)
        session.pop('reset_code', None)
        session.pop('reset_step', None)
        return redirect(url_for('reset_password'))
    
    # Handle resend code requests
    if request.args.get('resend') == '1' and 'reset_email' in session:
        email = session['reset_email']
        new_code = str(randint(100000, 999999))
        session['reset_code'] = new_code
        session['reset_step'] = 2  # Ensure we stay on step 2
        
        try:
            msg = Message("Password Reset Code",
                        recipients=[email])
            msg.body = f"Your new reset code is: {new_code}"
            mail.send(msg)
            flash("New code sent to your email", "success")
        except Exception as e:
            flash("Failed to resend code. Please try again.", "error")
        return redirect(url_for('reset_password'))
    
    # Initialize step (default to 1)
    step = session.get('reset_step', 1)

    if request.method == 'POST':
        if step == 1:
            email = request.form.get('email', '').strip()
            user = User.query.filter_by(email=email).first()
            
            if user:
                # Generate and store code
                reset_code = str(randint(100000, 999999))
                session.update({
                    'reset_email': email,
                    'reset_code': reset_code,
                    'reset_step': 2,
                    'code_timestamp': datetime.now().timestamp()
                })
                
                try:
                    msg = Message("Password Reset Code",
                                recipients=[email])
                    msg.body = f"Your reset code is: {reset_code}"
                    mail.send(msg)
                    flash("Reset code sent to your email", "success")
                except Exception as e:
                    flash("Failed to send email. Please try again.", "error")
                    session.pop('reset_email', None)
                    session.pop('reset_code', None)
                    session.pop('reset_step', None)
                    return redirect(url_for('reset_password'))
                
                return redirect(url_for('reset_password'))
            else:
                flash("Email not found", "error")
                return redirect(url_for('reset_password'))

        elif step == 2:
            user_code = request.form.get('code', '').strip()
            stored_code = session.get('reset_code')

            if user_code == stored_code:
                session['reset_step'] = 3
                return redirect(url_for('reset_password'))
            else:
                flash("Incorrect code", "error")

        elif step == 3:
            password = request.form.get('password')
            confirm = request.form.get('password_confirm')
            
            if len(password) < 8:
                flash("Password must be at least 8 characters", "error")
            elif password != confirm:
                flash("Passwords don't match", "error")
            else:
                email = session.get('reset_email')
                user = User.query.filter_by(email=email).first()
                if user:
                    user.set_password(password)
                    db.session.commit()
                    
                    # Clean up session
                    session.pop('reset_email', None)
                    session.pop('reset_code', None)
                    session.pop('reset_step', None)
                    session.pop('code_timestamp', None)
                    
                    flash("Password updated successfully!", "success")
                    return redirect(url_for('login'))
                else:
                    flash("Session expired", "error")
                    return redirect(url_for('reset_password'))
    
    # Additional GET validation
    if request.method == 'GET':
        if step == 2 and not all(k in session for k in ['reset_email', 'reset_code']):
            step = 1
            session.pop('reset_email', None)
            session.pop('reset_code', None)
            session.pop('reset_step', None)
    
    return render_template("resetPassword.html", 
                         csrf_token=csrf_token, 
                         step=step)

# User Input Route
@app.route('/submit', methods=['POST'])
@csrf.exempt
def submit():
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'status': 'error', 'message': 'User not logged in'}), 401

        data = request.json
        if not data:
            return jsonify({'status': 'error', 'message': 'No data received'}), 400

        record = UserInput(
            user_id=user_id,
            date=datetime.now().date(),
            exercise=data.get('exercise'),
            exercise_hours=to_float(data.get('exercise_hours')),
            water_intake=to_float(data.get('water_intake')),
            sleep_hours=to_float(data.get('sleep_hours')),
            reading_hours=to_float(data.get('reading_hours')),
            meals=to_int(data.get('meals')),
            screen_hours=to_float(data.get('screen_hours')),
            productivity=to_int(data.get('productivity')),
            mood=data.get('mood')
        )

        db.session.add(record)
        db.session.commit()

        session['last_input'] = data
        return jsonify({'status': 'success', 'message': 'Data submitted successfully.'})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
    
# Output Route
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    records = get_past_week_inputs(user_id)

    if not records:
        return render_template("Daily_output.html", message="No data found.")

    df = pd.DataFrame([{
        "date": r.date.strftime('%Y-%m-%d'),
        "exercise": 1 if r.exercise == "yes" else 0,
        "exercise_hours": r.exercise_hours or 0,
        "water": r.water_intake or 0,
        "sleep": r.sleep_hours or 0,
        "reading": r.reading_hours or 0,
        "screen": r.screen_hours or 0,
        "productivity": r.productivity or 0,
        "mood": r.mood or ""
    } for r in records])

    df.set_index("date", inplace=True)

    exercise_chart = generate_bar_chart(df["exercise_hours"].to_dict(), "Exercise Hours", "Hours")
    water_chart = generate_bar_chart(df["water"].to_dict(), "Water Intake", "Litres")
    sleep_chart = generate_bar_chart(df["sleep"].to_dict(), "Sleep Hours", "Hours")
    screen_vs_active = generate_pie_chart(df["screen"].sum(), max(0.1, df["exercise_hours"].sum() + df["reading"].sum()))

    streak = int(df["exercise"].sum())
    water_avg = df["water"].mean()
    sleep_avg = df["sleep"].mean()
    reading_total = int(df["reading"].sum() * 60)
    sleep_warning = sleep_avg < 7
    summary = (
        f"You exercised {df['exercise'].sum()} times, "
        f"slept an average of {sleep_avg:.1f} hrs "
        f"and had a peak mood. Great Job!!!"
    )

    return render_template("Daily_output.html",
                           exercise_chart=exercise_chart,
                           water_chart=water_chart,
                           sleep_chart=sleep_chart,
                           screen_chart=screen_vs_active,
                           streak=streak,
                           water_avg=f"{water_avg:.1f}",
                           sleep_avg=f"{sleep_avg:.1f}",
                           reading_total=reading_total,
                           sleep_warning=sleep_warning,
                           summary=summary)

# ResetPassword Clear Session
@app.route('/clear_reset_session', methods=['POST'])
def clear_reset_session():
    session.pop('reset_email', None)
    session.pop('reset_code', None)
    session.pop('reset_step', None)
    return '', 204

# When the user opens the website, it will automatically jump to the login page
@app.route('/')
def index():
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)