from flask import Blueprint, request, jsonify, session
from datetime import datetime
from models import db, UserInput
from extensions import csrf

input_bp = Blueprint('input', __name__)

@csrf.exempt
@input_bp.route('/submit', methods=['POST'])
def submit():
    try:
        data = request.json
        if not data:
            return jsonify({'status': 'error', 'message': 'No data received'}), 400

        record = UserInput(
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


