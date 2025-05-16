from app import app, db
from models import User
from test_config import TestConfig  

app.config.from_object(TestConfig)  

def run_server():
    with app.app_context():
        db.create_all()

        # Create a test user if it doesn't exist
        if not User.query.filter_by(email="testselenium@example.com").first():
            user = User(
                first_name="Selenium",
                last_name="Test",
                email="testselenium@example.com",
                phone="1234567890"
            )
            user.set_password("password123")
            db.session.add(user)
            db.session.commit()

        app.run(port=5000, debug=False, use_reloader=False)

if __name__ == '__main__':
    run_server()
