import unittest
from flask import json
from app import create_app
from user_model import db, User

MESSAGE = 'message'
USERS = 'users'
EMAIL = 'email'
USERNAME = 'username'
USER_CREATED = 'New user created'
USER_UPDATED = 'User updated'
INVALID_EMAIL = 'Invalid email address'
MISSING_DATA = 'Missing data'
USER_NOT_FOUND = 'User not found'


class UserRouteCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Add a user for testing
        self.test_user = User(username='wookie', email='wookie@cookie.com')
        db.session.add(self.test_user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data,
                         b'Welcome to the User Management Application. '
                         b'Navigate to /users to manage users.')

    def test_create_user(self):
        response = self.client.post('/users', json={
            'username': 'bfranklin1706',
            'first_name': 'Benjamin',
            'last_name': 'Franklin',
            'email': 'bfranklin1706@example.com'
        })
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data[MESSAGE], USER_CREATED)
        self.assertEqual(data['user'][USERNAME], 'bfranklin1706')
        self.assertEqual(data['user'][EMAIL], 'bfranklin1706@example.com')

    def test_get_user(self):
        response = self.client.get(f'/users/{self.test_user.username}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data[USERNAME], self.test_user.username)
        self.assertEqual(data[EMAIL], self.test_user.email)

    def test_get_users(self):
        response = self.client.get(f'/users')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data[USERS], list)
        self.assertGreaterEqual(len(data[USERS]), 1)

        users = {user[USERNAME]: user for user in data[USERS]}
        self.assertIn(self.test_user.username, users)
        self.assertEqual(users[self.test_user.username][EMAIL],
                         self.test_user.email)

    def test_get_users_with_sort_by_email(self):
        user1 = User(username='bwookie', email='bwookie@cookie.com')
        user2 = User(username='awookie', email='awookie@cookie.com')
        user3 = User(username='cwookie', email='cwookie@cookie.com')
        db.session.add_all([user1, user2, user3])
        db.session.commit()

        expected_emails = ['awookie@cookie.com',
                           'bwookie@cookie.com',
                           'cwookie@cookie.com',
                           'wookie@cookie.com']

        response = self.client.get('/users?sort=email')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)

        emails = [user[EMAIL] for user in data[USERS]]
        self.assertEqual(emails, expected_emails)

    def test_get_users_with_invalid_sort_by_key(self):
        response = self.client.get('/users?sort_by=invalid_key')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data[MESSAGE], 'Invalid sort_by parameter')

    def test_update_user_email_only(self):
        response = self.client.put(f'/users/{self.test_user.username}', json={
            'email': 'new_wookie@cookie.com'
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data[MESSAGE], USER_UPDATED)
        self.assertEqual(data['user'], self.test_user.username)

        response = self.client.get(f'/users')
        data = json.loads(response.data)

        for user in data[USERS]:
            if user[USERNAME] == self.test_user.username:
                self.assertEqual(user[EMAIL], 'new_wookie@cookie.com')

    def test_update_user(self):
        response = self.client.put(f'/users/{self.test_user.username}', json={
            'first_name': 'new_wookie',
            'last_name': 'new_cookie',
            'email': 'new_wookie@newcookie.com'
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['user'], self.test_user.username)
        self.assertEqual(data[MESSAGE], USER_UPDATED)

        response = self.client.get(f'/users')
        data = json.loads(response.data)

        for user in data[USERS]:
            if user[USERNAME] == self.test_user.username:
                self.assertEqual(user['first_name'], 'new_wookie')
                self.assertEqual(user['last_name'], 'new_cookie')
                self.assertEqual(user[EMAIL], 'new_wookie@newcookie.com')

    def test_create_user_without_username(self):
        response = self.client.post('/users', json={
            'first_name': 'Chuck',
            'last_name': 'Norris',
            'email': 'chuck@norris.com'
        })
        self.assertEqual(response.status_code, 400)  # Expect a 400 Bad Request
        data = json.loads(response.data)
        self.assertEqual(data[MESSAGE], MISSING_DATA)

    def test_create_user_with_invalid_username(self):
        response = self.client.post('/users', json={
            'username': 'non_alphanumeric@username',
            'first_name': 'Chuck',
            'last_name': 'Norris',
            'email': 'chuck@norris.com'
        })
        self.assertEqual(response.status_code, 400)  # Expect a 400 Bad Request
        data = json.loads(response.data)
        self.assertEqual(data[MESSAGE], 'Username must be alphanumeric')

    def test_create_user_with_invalid_email(self):
        response = self.client.post('/users', json={
            'username': 'cnorris1940',
            'first_name': 'Chuck',
            'last_name': 'Norris',
            'email': 'chuck@norris'
        })
        self.assertEqual(response.status_code, 400)  # Expect a 400 Bad Request
        data = json.loads(response.data)
        self.assertEqual(data[MESSAGE], INVALID_EMAIL)

    def test_create_user_with_existing_username(self):
        response = self.client.post('/users', json={
            'username': self.test_user.username,
            'first_name': 'Chuck',
            'last_name': 'Norris',
            'email': 'chuck@norris.com'
        })
        self.assertEqual(response.status_code, 400)  # Expect a 400 Bad Request
        data = json.loads(response.data)
        self.assertEqual(data[MESSAGE], 'Username already exists')

    def test_get_nonexistent_user(self):
        response = self.client.get('/users/cnorris1940')
        self.assertEqual(response.status_code, 404)  # Expect a 404 Not Found
        data = json.loads(response.data)
        self.assertEqual(data[MESSAGE], USER_NOT_FOUND)

    def test_update_nonexistent_user(self):
        response = self.client.put('/users/cnorris1940', json={
            'email': 'new_chuck@norris.com'
        })
        self.assertEqual(response.status_code, 404)  # Expect a 404 Not Found
        data = json.loads(response.data)
        self.assertEqual(data[MESSAGE], USER_NOT_FOUND)

    def test_update_invalid_email(self):
        response = self.client.put(f'/users/{self.test_user.username}', json={
            'email': 'wookie@cookie'
        })
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data[MESSAGE], INVALID_EMAIL)

    def test_update_user_without_data(self):
        response = self.client.put(f'/users/{self.test_user.username}',
                                   json={})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data[MESSAGE], MISSING_DATA)


if __name__ == '__main__':
    unittest.main()
