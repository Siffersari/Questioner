import unittest

from .base_test import BaseTest


class TestUsers(BaseTest):
    """ Contains all tests for user cases """

    def setUp(self):
        """ Sets up what the test will need before it runs """

        BaseTest.setUp(self)

    def test_register_user(self):
        """ Tests for user registration cases """

        new_user = self.register_user()

        self.assertEqual(new_user.status_code, 201)

    def test_login_user(self):
        """ Test cases for login in a user """

        self.register_user()

        self.assertEqual(self.login_user().status_code, 200)
        self.assertTrue(self.login_user().json["data"][0]["token"])

    def test_logout_user(self):
        """ Tests for successful log out of user """

        self.register_user()

        self.assertEqual(self.logout_user().status_code, 200)

    def test_fetch_user(self):
        """ Tests for successful fetch of user details """

        self.register_user()

        self.assertEqual(self.fetch_user_details().status_code, 200)

        self.assertTrue(self.fetch_user_details(
        ).json["data"][0]["username"] == 'Bjorn')

    def tearDown(self):
        """ Destroys set up data before running each test """

        BaseTest.tearDown(self)


if __name__ == "__main__":

    unittest.main()
