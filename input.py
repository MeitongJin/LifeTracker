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
            exercise_hours=float(data.get('exercise_hours', 0)),
            water_intake=float(data.get('water_intake', 0)),
            sleep_hours=float(data.get('sleep_hours', 0)),
            reading_hours=float(data.get('reading_hours', 0)),
            meals=int(data.get('meals', 0)),
            screen_hours=float(data.get('screen_hours', 0)),
            productivity=int(data.get('productivity', 0)),
            mood=data.get('mood')
        )

        db.session.add(record)
        db.session.commit()

        session['last_input'] = data
        return jsonify({'status': 'success', 'message': 'Data submitted successfully.'})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


