import unittest
from app import app, db
from models import User

class TestLifeTrackerApp(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.drop_all()

    # 1. Test the home page（The /home route redirects users to the login page if they are not authenticated）
    def test_home_redirects_when_not_logged_in(self):
        response = self.client.get('/home', follow_redirects=False)
        self.assertEqual(response.status_code, 302)

    # 2. Test the register page （User registration process）
    def test_register_user(self):
        response = self.client.post('/register', data={
            'firstname': 'Alice',
            'lastname': 'Smith',
            'email': 'alice@example.com',
            'phone': '1234567890',
            'password': 'password123',
            'password_confirm': 'password123'
        }, follow_redirects=True)
        self.assertIn(b'Registration successful', response.data)

    # 3. Test the login page（User login process）
    def test_login_user(self):
        with app.app_context():
            user = User(first_name='Bob', last_name='Lee', email='bob@example.com', phone='1234567890')
            user.set_password('password123')
            db.session.add(user)
            db.session.commit()
        response = self.client.post('/login', data={
            'email': 'bob@example.com',
            'password': 'password123'
        }, follow_redirects=True)
        self.assertIn(b'Login successful', response.data)

    # 4. Test the /submit data submission（Whether the data submission of unlogged-in users is rejected）
    def test_submit_without_login(self):
        response = self.client.post('/submit', json={
            'exercise': 'yes', 'exercise_hours': 1, 'water_intake': 2,
            'sleep_hours': 8, 'reading_hours': 1, 'meals': 3,
            'screen_hours': 4, 'productivity': 7, 'mood': '😊'
        })
        self.assertEqual(response.status_code, 401)

    # 5. Test the /resetPassword page（Enter the unregistered email address in the password reset request）
    def test_reset_password_step1_invalid_email(self):
        response = self.client.post('/resetPassword', data={'email': 'notfound@example.com'}, follow_redirects=True)
        self.assertIn(b'Email not found', response.data)

    # 6. Test /submit（Successfully submit data in the logged-in state）
    def test_submit_with_login(self):
        with app.app_context():
            user = User(first_name='D', last_name='W', email='dw@example.com', phone='1234567890')
            user.set_password('abc123456')
            db.session.add(user)
            db.session.commit()
            user_id = user.id

        with self.client.session_transaction() as sess:
            sess['user_id'] = user_id

        response = self.client.post('/submit', json={
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

    # 7. Test /daily_output page logic（Whether the log page prompts correctly when there is no data）
    def test_output_page_no_data(self):
        with app.app_context():
            user = User(first_name='E', last_name='F', email='ef@example.com', phone='1234567890')
            user.set_password('abc123456')
            db.session.add(user)
            db.session.commit()

        with self.client.session_transaction() as sess:
            sess['user_id'] = user.id

        response = self.client.get('/daily_output')
        self.assertIn(b'No data found', response.data)
        
    # 8. Test /dashboard requires login（Not logged in to access /dashboard whether to redirect）
    def test_dashboard_redirect_if_not_logged_in(self):
        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.headers['Location'])

    # 9. Test clear_reset_session works（/Clear_reset_session Whether to clear session）
    def test_clear_reset_session(self):
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

    # 10. Test resetPassword Step 1 with valid email（Retrieve password Step1: Whether to update the valid mailbox session）
    def test_reset_password_step1_valid_email(self):
        # Create user
        with app.app_context():
            user = User(first_name='Reset', last_name='Test', email='reset@example.com', phone='1234567890')
            user.set_password('password123')
            db.session.add(user)
            db.session.commit()

        response = self.client.post('/resetPassword', data={
            'email': 'reset@example.com'
        }, follow_redirects=True)

        # We can't really test email sending here, but we can confirm session updated
        with self.client.session_transaction() as sess:
            self.assertEqual(sess['reset_email'], 'reset@example.com')
            self.assertEqual(sess['reset_step'], 2)
            self.assertTrue('reset_code' in sess)


if __name__ == '__main__':
    unittest.main()
