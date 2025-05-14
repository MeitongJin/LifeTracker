from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_migrate import Migrate # Import Migrate
from flask_wtf.csrf import generate_csrf
import re
from random import randint
from flask_mail import Mail, Message
import pandas as pd
import matplotlib
# matplotlib.use('Agg')  # Prohibit the use of GUI back-end to prevent crashes 
# import matplotlib.pyplot as plt
import io
import base64
# Custom modules
from extensions import db, csrf
from models import User, UserInput, SharedAccess
from input import to_float, to_int
from output import get_past_week_inputs, generate_bar_chart, generate_pie_chart
from datetime import datetime, timedelta, date
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)

# Email configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'team.lifetracker@gmail.com'  
app.config['MAIL_PASSWORD'] = 'otre nlsm fdcj josn'
app.config['MAIL_DEFAULT_SENDER'] = 'team.lifetracker@gmail.com'  

mail = Mail(app)

app.config['SECRET_KEY'] = '96116a385604fce2551eabb56cf90b03'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lifetracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_COOKIE_SECURE'] = False  # For development (True for production)
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

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
    
def get_user_inputs(user_id, days=7):
    """Get user inputs for specified number of days"""
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days-1)
    
    return UserInput.query.filter(
        UserInput.user_id == user_id,
        UserInput.date >= start_date,
        UserInput.date <= end_date
    ).order_by(UserInput.date).all()

def prepare_exercise_data(records):
    return {
        'hours': [r.exercise_hours or 0 for r in records],
        'days': [r.exercise == 'yes' for r in records]
    }

def prepare_water_data(records):
    return [r.water_intake or 0 for r in records]

def prepare_sleep_data(records):
    return [r.sleep_hours or 0 for r in records]

def prepare_screen_data(records):
    return [r.screen_hours or 0 for r in records]
    
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
        firstname = request.form.get('firstname', '').strip()
        lastname = request.form.get('lastname', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()  # Added default empty string
        password = request.form.get('password', '')
        password_confirm = request.form.get('password_confirm', '')   

        # Validation
        if not firstname:
            errors['firstname'] = 'First name is required.'
        if not lastname:
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
                                   firstname=firstname, lastname=lastname,
                                   email=email, phone=phone)

        # Create new user
        new_user = User(
            first_name=firstname,
            last_name=lastname,
            email=email,
            phone=phone
        )
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', errors={}, firstname='', lastname='', email='', phone='')

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
@app.route('/daily_input')
def daily_input():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('Daily_input.html',user_name=session.get('user_name'))

# User Input Submission - Updated to overwrite existing entries
@app.route('/submit', methods=['POST'])
@csrf.exempt
def submit():
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'status': 'error', 'message': 'User not logged in'}), 401

        # Ensure request is JSON
        if not request.is_json:
            return jsonify({'status': 'error', 'message': 'Request must be JSON'}), 400

        data = request.get_json()
        if not data:
            return jsonify({'status': 'error', 'message': 'No data received'}), 400

        today = date.today()
        
        # Check for existing record
        existing_record = UserInput.query.filter_by(
            user_id=user_id,
            date=today
        ).first()

        if existing_record:
            # Update existing record
            existing_record.exercise = data.get('exercise', existing_record.exercise)
            existing_record.exercise_hours = to_float(data.get('exercise_hours', existing_record.exercise_hours))
            existing_record.water_intake = to_float(data.get('water_intake', existing_record.water_intake))
            existing_record.sleep_hours = to_float(data.get('sleep_hours', existing_record.sleep_hours))
            existing_record.reading_hours = to_float(data.get('reading_hours', existing_record.reading_hours))
            existing_record.meals = to_int(data.get('meals', existing_record.meals))
            existing_record.screen_hours = to_float(data.get('screen_hours', existing_record.screen_hours))
            existing_record.productivity = to_int(data.get('productivity', existing_record.productivity))
            existing_record.mood = data.get('mood', existing_record.mood)
            message = 'Data updated successfully.'
        else:
            # Create new record
            record = UserInput(
                user_id=user_id,
                date=today,
                exercise=data.get('exercise', 'no'),
                exercise_hours=to_float(data.get('exercise_hours', 0)),
                water_intake=to_float(data.get('water_intake', 0)),
                sleep_hours=to_float(data.get('sleep_hours', 0)),
                reading_hours=to_float(data.get('reading_hours', 0)),
                meals=to_int(data.get('meals', 0)),
                screen_hours=to_float(data.get('screen_hours', 0)),
                productivity=to_int(data.get('productivity', 0)),
                mood=data.get('mood', '')
            )
            db.session.add(record)
            message = 'Data submitted successfully.'

        db.session.commit()
        return jsonify({'status': 'success', 'message': message})

    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500
    
# Output Route
@app.route('/daily_output', methods=['GET'])
def daily_output():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    selected_date = request.args.get('selected_date')

    if selected_date:
        try:
            selected_date_obj = datetime.strptime(selected_date, '%Y-%m-%d').date()
            # Fetch records for the selected date only
            records = UserInput.query.filter(
                UserInput.user_id == user_id,
                UserInput.date == selected_date_obj
            ).all()
        except ValueError:
            records = []  # Invalid date format fallback
    else:
        # No date selected: fetch all records up to today (or past week if preferred)
        records = UserInput.query.filter(
            UserInput.user_id == user_id,
            UserInput.date <= datetime.today().date()
        ).order_by(UserInput.date).all()

    if not records:
        return render_template("Daily_output.html", message="No data found.", selected_date=selected_date or "", user_name=session.get('user_name'))

    # Prepare data for the charts
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

    # Generate chart data
    exercise_labels = df.index.tolist()
    exercise_data = df["exercise_hours"].tolist()
    water_labels = df.index.tolist()
    water_data = df["water"].tolist()
    sleep_labels = df.index.tolist()
    sleep_data = df["sleep"].tolist()
    screen_labels = df.index.tolist()
    screen_data = df["screen"].tolist()

    # Generate charts as base64 strings
    exercise_chart = generate_bar_chart(dict(zip(exercise_labels, exercise_data)), "Exercise Hours", "Hours")
    water_chart = generate_bar_chart(dict(zip(water_labels, water_data)), "Water Intake", "Litres")
    sleep_chart = generate_bar_chart(dict(zip(sleep_labels, sleep_data)), "Sleep Hours", "Hours")
    screen_vs_active = generate_pie_chart(sum(screen_data), max(0.1, sum(df["exercise_hours"]) + sum(df["reading"])))

    streak = int(df["exercise"].sum())
    water_avg = df["water"].mean()
    sleep_avg = df["sleep"].mean()
    reading_total = int(df["reading"].sum() * 60)
    reading_today = df.iloc[-1]["reading"] if not df.empty else 0

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
                           reading_hours=reading_today,
                           sleep_warning=sleep_warning,
                           summary=summary, 
                           user_name=session.get('user_name'),
                           exercise_labels=exercise_labels,
                           exercise_data=exercise_data,
                           water_labels=water_labels,
                           water_data=water_data,
                           sleep_labels=sleep_labels,
                           sleep_data=sleep_data,
                           screen_labels=screen_labels,
                           screen_data=screen_data,
                           selected_date=selected_date)



@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # Get the user inputs for the selected range (7 or 30 days)
    range = request.args.get('range', '7')
    user_inputs = get_user_inputs(session['user_id'], days=int(range))

    # Get list of people the current user has shared with
    shared_with = SharedAccess.query.filter_by(owner_id=session['user_id'])\
        .join(User, SharedAccess.viewer_id == User.id).all()

    # Prepare the data for the charts
    exercise_data = prepare_exercise_data(user_inputs)
    water_data = prepare_water_data(user_inputs)
    sleep_data = prepare_sleep_data(user_inputs)
    screen_data = prepare_screen_data(user_inputs)
    dates = [input.date.strftime('%Y-%m-%d') for input in user_inputs]

    chart_data = {
        'exercise': exercise_data['hours'],
        'water': water_data,
        'sleep': sleep_data,
        'screen': screen_data
    }

    
    return render_template('dashboard.html', 
                         chart_data=chart_data, 
                         current_range=range,
                         dates=dates,
                         shared_with=shared_with)

@app.route('/share_view', methods=['GET'])
def share_view():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    viewer_id = session['user_id']

    # Get list of users who have shared with this viewer
    shared_users = db.session.query(User).join(SharedAccess, SharedAccess.owner_id == User.id)\
        .filter(SharedAccess.viewer_id == viewer_id).all()

    # Get selected user and range
    selected_user_id = request.args.get('user_id', type=int)
    range_days = request.args.get('range', 7, type=int)

    chart_data = {
        'exercise': [],
        'water': [],
        'sleep': [],
        'screen': [],
        'dates': []
    }
    viewing_user = None

    if selected_user_id:
        access = SharedAccess.query.filter_by(owner_id=selected_user_id, viewer_id=viewer_id).first()
        if access:
            inputs = get_user_inputs(selected_user_id, days=range_days)
            chart_data = {
                'exercise': prepare_exercise_data(inputs)['hours'],
                'water': prepare_water_data(inputs),
                'sleep': prepare_sleep_data(inputs),
                'screen': prepare_screen_data(inputs),
                'dates': [r.date.strftime('%Y-%m-%d') for r in inputs]
            }
            viewing_user = User.query.get(selected_user_id)

    return render_template('share-view.html',
                           shared_users=shared_users,
                           chart_data=chart_data,
                           selected_user_id=selected_user_id,
                           viewing_user=viewing_user,
                           range_days=range_days)



@app.route('/share_dashboard', methods=['POST'])
def share_dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if not request.form:  # Check if form data exists
        flash("No form data submitted", "danger")
        return redirect(url_for('dashboard'))

    viewer_email = request.form.get('viewer_email', '').strip().lower()
    if not viewer_email:  # Validate email is provided
        flash("Please enter an email address", "danger")
        return redirect(url_for('dashboard'))

    try:
        viewer = User.query.filter_by(email=viewer_email).first()
        owner_id = session['user_id']

        if not viewer:
            flash("User not found.", "danger")
        elif viewer.id == owner_id:
            flash("You can't share with yourself.", "warning")
        else:
            # Check if already shared
            existing = SharedAccess.query.filter_by(owner_id=owner_id, viewer_id=viewer.id).first()
            if existing:
                flash("Already shared with this user.", "info")
            else:
                new_access = SharedAccess(owner_id=owner_id, viewer_id=viewer.id)
                db.session.add(new_access)
                db.session.commit()
                flash("Dashboard shared successfully!", "success")

    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error sharing dashboard: {str(e)}")
        flash("An error occurred while sharing. Please try again.", "danger")

    return redirect(url_for('dashboard'))


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