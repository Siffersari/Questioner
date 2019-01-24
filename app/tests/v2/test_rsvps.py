import unittest
import json
import os
from ... import create_app
from ... db_con import create_tables, destroy_database


class TestQuestions(unittest.TestCase):
    """
    Contains testcases for questions 
    for a meetup record
    """

    def setUp(self):
        """ Sets up what the test will need before it runs """

        self.app = create_app("testing")

        self.client = self.app.test_client()

        os.environ["DATABASE_URL"] = os.getenv("DATABASE_TESTING_URL")

        create_tables()

        self.data = {
            "firstname": "User",
            "lastname": "Test",
            "othername": "UserTest",
            "email": "test@test.com",
            "phoneNumber": "0712332112",
            "username": "testuser",
            "password": "P@5sword",
            "confirmPass": "P@5sword"
        }

        self.meetup = {
            "location": "Angle House, Nairobi",
            "images": ["img1.jgp", "img2.jpg"],
            "topic": "Do It Yourself",
            "happeningOn": "Feb 4 2019 10:30AM",
            "tags": ["Creative", "Technology"],
            "user": 1
        }

        self.rsvp = {
            "user": 1,
            "response": "yes"
        }

        self.content_type = "application/json"

        self.user = self.client.post("/api/v2/auth/signup",
                                     data=json.dumps(self.data), content_type="application/json")

        login = self.login_user()

        self.assertEqual(login.status_code, 200)

        self.assertTrue(self.login_user().json["data"][0]["token"])

        self.headers = {'Authorization': 'Bearer {}'.format(
            login.json["data"][0]["token"])}

        self.create_meetup()

    def login_user(self, path="/api/v2/auth/login", data={}):
        """ Logs in a user if registered """

        if not data:
            data = self.data

        response = self.client.post(path, data=json.dumps(
            data), content_type="application/json")

        return response

    def create_meetup(self, path="api/v2/meetups", data={}):
        """ Creates a meetup """

        if not data:
            data = self.meetup

        response = self.client.post(path, data=json.dumps(
            data), content_type=self.content_type, headers=self.headers)

        return response

    def respond_meetup(self, path="/api/v2/meetups/<int:meetup_id>/rsvps", data={}):
        """ Responds to meetup RSVP """

        if not data:
            data = self.rsvp

        response = self.client.post(path, data=json.dumps(
            data), content_type="application/json", headers=self.headers)

        return response

    def test_respond_meetup(self):
        """ Tests for responding to a meetup """

        rsvp = self.respond_meetup(path="/api/v2/meetups/1/rsvps")

        self.assertEqual(rsvp.status_code, 201)

    def tearDown(self):
        """ Destroys set up data before running each test """

        destroy_database()

    os.environ["DATABASE_URL"] = "dbname='questioner' host='localhost' port='5432' user='leewel' password='root'"


if __name__ == "__main__":

    unittest.main()
