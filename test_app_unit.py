import unittest
from app import app, db
from models import User
from flask_wtf.csrf import generate_csrf
from flask import url_for, session

class TestLifeTrackerApp(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
        app.config['SERVER_NAME'] = 'localhost'  # Required for url_for
        
        self.client = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_home_redirects_when_not_logged_in(self):
        response = self.client.get('/home', follow_redirects=False)
        self.assertEqual(response.status_code, 302)

    def test_register_user(self):
        response = self.client.post('/register', 
            data={
                'firstname': 'Alice',
                'lastname': 'Smith',
                'email': 'alice@example.com',
                'phone': '1234567890',
                'password': 'password123',
                'password_confirm': 'password123'
            }, 
            follow_redirects=True)
        
        # Check for either flash message OR redirect to login page
        self.assertTrue(
            b'Registration successful' in response.data or
            b'Log In to Life Tracker' in response.data,
            "Should show success message or redirect to login"
        )
        
        # Verify user was actually created
        with app.app_context():
            user = User.query.filter_by(email='alice@example.com').first()
            self.assertIsNotNone(user, "User should exist in database")

    def test_login_user(self):
        with app.app_context():
            # Create test user
            user = User(first_name='Bob', last_name='Lee', 
                    email='bob@example.com', phone='1234567890')
            user.set_password('password123')
            db.session.add(user)
            db.session.commit()
            
            # Test login
            response = self.client.post('/login', 
                data={
                    'email': 'bob@example.com',
                    'password': 'password123'
                }, 
                follow_redirects=True)
            
            # Check for either flash message OR successful redirect content
            self.assertTrue(
                b'Login successful' in response.data or 
                b'Good' in response.data and b'Bob' in response.data,
                "Login should either show success message or redirect to dashboard"
            )

    def test_submit_without_login(self):
        response = self.client.post('/submit', 
            json={
                'exercise': 'yes', 
                'exercise_hours': 1, 
                'water_intake': 2,
                'sleep_hours': 8, 
                'reading_hours': 1, 
                'meals': 3,
                'screen_hours': 4, 
                'productivity': 7, 
                'mood': '😊'
            })
        self.assertEqual(response.status_code, 401)

    def test_reset_password_step1_invalid_email(self):
        response = self.client.post('/resetPassword', 
            data={
                'email': 'notfound@example.com'
            }, 
            follow_redirects=True)
        self.assertIn(b'Email not found', response.data)

    def test_submit_with_login(self):
        with app.app_context():
            user = User(first_name='D', last_name='W', 
                       email='dw@example.com', phone='1234567890')
            user.set_password('abc123456')
            db.session.add(user)
            db.session.commit()
            
            with self.client.session_transaction() as sess:
                sess['user_id'] = user.id

            response = self.client.post('/submit', 
                json={
                    'exercise': 'yes',
                    'exercise_hours': 1.5,
                    'water_intake': 2,
                    'sleep_hours': 8,
                    'reading_hours': 1,
                    'meals': 3,
                    'screen_hours': 4,
                    'productivity': 7,
                    'mood': '😊'
                })
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'success', response.data)

    def test_output_page_no_data(self):
        with app.app_context():
            user = User(first_name='E', last_name='F', 
                       email='ef@example.com', phone='1234567890')
            user.set_password('abc123456')
            db.session.add(user)
            db.session.commit()
            
            with self.client.session_transaction() as sess:
                sess['user_id'] = user.id

            response = self.client.get('/daily_output')
            self.assertIn(b'No data found', response.data)
        
    def test_dashboard_redirect_if_not_logged_in(self):
        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.headers['Location'])

    def test_clear_reset_session(self):
        with app.app_context():
            with self.client.session_transaction() as sess:
                sess['reset_email'] = 'test@example.com'
                sess['reset_code'] = '123456'
                sess['reset_step'] = 2

            response = self.client.post('/clear_reset_session')
            self.assertEqual(response.status_code, 204)

            with self.client.session_transaction() as sess:
                self.assertNotIn('reset_email', sess)
                self.assertNotIn('reset_code', sess)
                self.assertNotIn('reset_step', sess)

    def test_reset_password_step1_valid_email(self):
        with app.app_context():
            user = User(first_name='Reset', last_name='Test', 
                       email='reset@example.com', phone='1234567890')
            user.set_password('password123')
            db.session.add(user)
            db.session.commit()

            response = self.client.post('/resetPassword', 
                data={
                    'email': 'reset@example.com'
                }, 
                follow_redirects=True)

            with self.client.session_transaction() as sess:
                self.assertEqual(sess['reset_email'], 'reset@example.com')
                self.assertEqual(sess['reset_step'], 2)
                self.assertIn('reset_code', sess)

if __name__ == '__main__':
    unittest.main()