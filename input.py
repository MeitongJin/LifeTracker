from flask import Blueprint, request, jsonify, session
from datetime import datetime
from models import db, UserInput
from extensions import csrf

input_bp = Blueprint('input', __name__)

@csrf.exempt
@input_bp.route('/submit', methods=['POST'])
def submit():
    try:
        # Get the current login user ID
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'status': 'error', 'message': 'User not logged in'}), 401

        data = request.json
        if not data:
            return jsonify({'status': 'error', 'message': 'No data received'}), 400
        
        # Validate required fields
        # Convert data to appropriate types, prevent data formatting errors, avoid service interruption due to type error
        def to_float(val):
            try:
                return float(val)
            except (TypeError, ValueError):
                return 0.0

        def to_int(val):
            try:
                return int(val)
            except (TypeError, ValueError):
                return 0

        record = UserInput(
            user_id=user_id,
            date=datetime.now().date(),
            exercise=data.get('exercise'),
            exercise_hours=to_float(data.get('exercise_hours')),  # Use the previously defined to_float and to_int to handle exceptions and empty values
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


