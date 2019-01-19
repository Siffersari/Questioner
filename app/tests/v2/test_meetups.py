import unittest
import json
import os
from ... import create_app
from ... db_con import create_tables, destroy_database


class TestMeetups(unittest.TestCase):
    """ Contains all tests for meetup cases """

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
            "password": "P@5sword"
        }

        self.meetup = {
            "location": "Angle House, Nairobi",
            "images": ["img1.jgp", "img2.jpg"],
            "topic": "Do It Yourself",
            "happeningOn": "Feb 4 2019 10:30AM",
            "tags": ["Creative", "Technology"],
            "user": 1
        }

        self.missing = {
            "location": "Jungle House, Mombase",
            "images": ["img1.jgp", "img2.jpg"],
            "happeningOn": "Jan 13 2019 10:30AM",
            "tags": ["Creative", "Technology"],
            "user": 1
        }

        self.imageless = {
            "location": "Angle House, Nairobi",
            "topic": "Go Imagesless",
            "happeningOn": "Feb 15 2019 10:30AM",
            "tags": ["Creative"],
            "user": 1
        }

        self.content_type = "application/json"

        self.user = self.client.post("/api/v2/auth/signup",
                                     data=json.dumps(self.data), content_type="application/json")

        login = self.login_user()

        self.assertEqual(login.status_code, 200)

        self.assertTrue(self.login_user().json["data"][0]["token"])

        self.headers = {'Authorization': 'Bearer {}'.format(
            login.json["data"][0]["token"])}

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

    def delete_meetup(self, path="api/v2/meetups/<meetup-id>", data={}):
        """ Deletes a meetup """

        if not data:
            data = {
                "user": 1
            }

        response = self.client.delete(path, data=json.dumps(
            data), content_type=self.content_type, headers=self.headers)

        return response

    def post_images(self, path="api/v2/meetups/<meetup-id>/images", data={}):
        """ Adds images to meetup """

        if not data:
            data = {
                "user": 1,
                "images": ["tumbl.url.com", "insta.com"]
            }

        response = self.client.post(path, data=json.dumps(
            data), content_type=self.content_type, headers=self.headers)

        return response

    def add_tags(self, path="api/v2/meetups/<meetup-id>/tags", data={}):
        """ Adds images to meetup """

        if not data:
            data = {
                "user": 1,
                "tags": ["Instagram", "ruby"]
            }

        response = self.client.post(path, data=json.dumps(
            data), content_type=self.content_type, headers=self.headers)

        return response

    def fetch_specific_meetup(self, path="/api/v2/meetups/<meetup-id>"):
        """ Fetches a specific meetup record """

        response = self.client.get(path, headers=self.headers)

        return response

    def fetch_upcoming_meetup(self, path="/api/v1/meetups/upcoming"):

        response = self.client.get(path, headers=self.headers)

        return response

    def test_create_new_meetup(self):
        """ Test cases for creating  a new meetup """

        new_meetup = self.create_meetup()

        self.assertEqual(new_meetup.status_code, 201)

    def test_raises_badrequest_if_required_missing(self):
        """ 
        Test for Badrequest when a required field is missing
        """

        missing_topic = self.create_meetup(data=self.missing)

        self.assertEqual(missing_topic.status_code, 400)
        self.assertTrue(missing_topic.json["error"])

    def test_creates_meetup_if_missing_images_key(self):
        """ 
        Test whether new meetup is created if images key
        are not provided 
        """

        missing_images = self.create_meetup(data=self.imageless)

        self.assertEqual(missing_images.status_code, 201)
        self.assertTrue(missing_images.json["data"])

    def test_fetches_meetup_record_if_correct_id(self):
        """
        Tests that endpoint fetches a specific meetup record if
        provided data is correct 
        """

        meetup_1 = self.create_meetup()

        self.assertEqual(meetup_1.status_code, 201)
        self.assertTrue(meetup_1.json["data"])

        self.assertEqual(self.fetch_specific_meetup(
            path="/api/v2/meetups/1").status_code, 200)
        self.assertTrue(self.fetch_specific_meetup(
            path="/api/v2/meetups/1").json["data"])
        self.assertNotEqual(self.fetch_specific_meetup(
            path="/api/v2/meetups/1").status_code, 404)

    def test_fetches_upcoming_meetup(self):
        """
        Tests fetch all ucpcoming meetups
        """
        self.create_meetup()

        self.assertEqual(self.fetch_upcoming_meetup(
            path="/api/v2/meetups/upcoming").status_code, 200)
        self.assertTrue(self.fetch_upcoming_meetup(
            path="/api/v2/meetups/upcoming").json["data"])
        self.assertNotEqual(self.fetch_upcoming_meetup(
            path="/api/v2/meetups/upcoming").status_code, 404)

    def test_delete_existing_meetup(self):
        """ Test cases for deleting a meetup """

        new_meetup = self.create_meetup()

        self.assertEqual(new_meetup.status_code, 201)

        self.assertEqual(self.delete_meetup(
            path="api/v2/meetups/1").status_code, 200)

        self.assertEqual(self.delete_meetup(
            path="api/v2/meetups/1").status_code, 404)

        self.assertTrue(self.delete_meetup(
            path="api/v2/meetups/1").json["error"])

    def test_posts_images(self):
        """ Tests for posting meetup """

        new_meetup = self.create_meetup()

        self.assertEqual(new_meetup.status_code, 201)

        self.assertEqual(self.post_images(
            path="/api/v2/meetups/1/images").status_code, 201)

        self.assertTrue(self.post_images(
            path="/api/v2/meetups/1/images").json["data"][0]["images"])

    def test_raises_error_if_missing_meetup(self):
        """ Tests for failure if missing meetup """

        self.assertEqual(self.post_images(
            path="/api/v2/meetups/1/images").status_code, 404)

        self.assertTrue(self.post_images(
            path="/api/v2/meetups/1/images").json["error"])

    def test_raises_error_if_missing_user(self):
        """ Test for failure if missing user """

        data = {
            "user": 99,
            "images": ["this"]
        }

        self.assertEqual(self.post_images(
            path="/api/v2/meetups/1/images", data=data).status_code, 404)

    def test_add_tags(self):
        """ Tests for posting meetup """

        new_meetup = self.create_meetup()

        self.assertEqual(new_meetup.status_code, 201)

        self.assertEqual(self.add_tags(
            path="/api/v2/meetups/1/tags").status_code, 201)

        self.assertTrue(self.add_tags(
            path="/api/v2/meetups/1/tags").json["data"][0]["tags"])

    def test_raises_Notfound_if_missing_meetup(self):
        """ Tests for failure if missing meetup """

        self.assertEqual(self.add_tags(
            path="/api/v2/meetups/1/tags").status_code, 404)

        self.assertTrue(self.add_tags(
            path="/api/v2/meetups/1/tags").json["error"])

    def test_raises_NotFound_if_missing_user(self):
        """ Test for failure if missing user """

        data = {
            "user": 99,
            "tags": ["tags"]
        }

        self.assertEqual(self.add_tags(
            path="/api/v2/meetups/1/tags", data=data).status_code, 404)

    def tearDown(self):
        """ Destroys set up data before running each test """

        destroy_database()

    os.environ["DATABASE_URL"] = "dbname='questioner' host='localhost' port='5432' user='leewel' password='root'"


if __name__ == "__main__":

    unittest.main()
