from extensions import db


# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        from werkzeug.security import generate_password_hash
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password_hash, password)

# Users input data model(every day)
class UserInput(db.Model):
    __tablename__ = 'user_inputs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_userinput_user_id'), nullable=False) # Add foreign key to link with user
    date = db.Column(db.Date, nullable=False)
    exercise = db.Column(db.String(10))              # "yes" or "no"
    exercise_hours = db.Column(db.Float)             # e.g., 1.5
    water_intake = db.Column(db.Float)               # e.g., 2.0 
    sleep_hours = db.Column(db.Float)
    reading_hours = db.Column(db.Float)
    meals = db.Column(db.Integer)
    screen_hours = db.Column(db.Float)
    productivity = db.Column(db.Integer)             # 1 to 10
    mood = db.Column(db.String(20))                  # e.g., "happy"


