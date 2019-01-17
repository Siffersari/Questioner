import unittest
import json
from ... import create_app
from ... db_con import init_test_db, destroy_database


class TestUsers(unittest.TestCase):
    """ Contains all tests for user cases """

    def setUp(self):
        """ Sets up what the test will need before it runs """

        self.app = create_app("testing")
        self.client = self.app.test_client()

        with self.app.app_context():
            self.db = init_test_db()

        self.data = {
            "firstname": "User",
            "lastname": "Test",
            "othername": "UserTest",
            "email": "test@test.com",
            "phoneNumber": "0712332112",
            "username": "testuser",
            "password": "P@5sword"
        }

    def register_user(self, path="/api/v2/auth/signup", data={}):
        """ Registers a new user given data or default if not provided"""

        if not data:
            data = self.data

        response = self.client.post(path, data=json.dumps(
            data), content_type="application/json")

        return response

    def login_user(self, path="/api/v2/auth/login", data={}):
        """ Logs in a user if registered """

        if not data:
            data = self.data

        response = self.client.post(path, data=json.dumps(
            data), content_type="application/json")

        return response

    def test_register_user(self):
        """ Tests for user registration cases """

        new_user = self.register_user()

        self.assertEqual(new_user.status_code, 201)

    def test_login_user(self):
        """ Test cases for login in a user """

        self.register_user()

        self.assertEqual(self.login_user().status_code, 200)

    def tearDown(self):
        """ Destroys set up data before running each test """
        with self.app.app_context():
            destroy_database()
            self.db.close()


if __name__ == "__main__":

    unittest.main()
