from unittest import TestCase
from app import app
from models import db, User
from dotenv import load_dotenv
import os

load_dotenv()

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('TEST_DATABASE_URL')
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

class UserViewsTestCase(TestCase):
    """Tests for views for Users."""

    @classmethod
    def setUpClass(cls):
        """Set up the database once for all tests."""
        with app.app_context():
            db.drop_all()
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        """Clean up the database after all tests."""
        with app.app_context():
            db.drop_all()

    def setUp(self):
        """Add sample user."""
        with app.app_context():
            User.query.delete()

            user = User(first_name="Test", last_name="User")
            db.session.add(user)
            db.session.commit()

            self.user_id = user.id
            self.user = user

    def tearDown(self):
        """Clean up any fouled transaction."""
        with app.app_context():
            db.session.rollback()

    def test_list_all_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test User', html)

    def test_add_user(self):
        with app.test_client() as client:
            u = {'first': 'User', 'last': 'Two', 'pic-url': 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?q=80&w=2670&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'}
            resp = client.post("/users/new", data=u, follow_redirects=True)
            html = resp.get_data(as_text=True)

             # Debugging: Print response data
            print(f"Response status: {resp.status_code}")
            print(f"Response data: {html}")

            self.assertEqual(resp.status_code, 200)
            self.assertIn('User Two', html)

    def test_single_user(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test User', html)

    def test_delete_user(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('Test User', html)


if __name__ == '__main__':
    import unittest
    unittest.main()
