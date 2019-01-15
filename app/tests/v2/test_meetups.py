import unittest
import json
from ... import create_app
from ... db_con import create_tables, destroy_database


class TestMeetups(unittest.TestCase):
    """
    Contains test cases for the meetups
    """

    def setUp(self):
        """ Sets up what the test will need before it runs """

        self.app = create_app()

        self.client = self.app.test_client()

        self.db = create_tables(db_type="testing")

        self.data = {
            "location": "Angle House, Nairobi",
            "images": ["img1.jgp", "img2.jpg"],
            "topic": "Do It Yourself",
            "happeningOn": "Feb 4 2019 10:30AM",
            "tags": ["Creative", "Technology"],
            "username": "Leewel"

        }
        self.missing = {
            "location": "Jungle House, Mombase",
            "images": ["img1.jgp", "img2.jpg"],
            "happeningOn": "Jan 13 2019 10:30AM",
            "tags": ["Creative", "Technology"],
            "username": "Nani"
        }

        self.imageless = {
            "location": "Angle House, Nairobi",
            "topic": "Go Imagesless",
            "happeningOn": "Feb 15 2019 10:30AM",
            "tags": ["Creative"],
            "username": "Photographer"
        }

    def create_meetup(self, path="api/v2/meetups", data={}):
        """ Creates a meetup """
        if not data:
            data = self.data

        response = self.client.post(path, data=json.dumps(
            data), content_type="application/json")

        return response

    def fetch_specific_meetup(self, path="/api/v2/meetups/<meetup-id>"):
        """ Fetches a specific meetup record """

        response = self.client.get(path)

        return response

    def fetch_upcoming_meetup(self, path="/api/v2/meetups/upcoming"):

        response = self.client.get(path)

        return response

    def test_create_new_meetup(self):
        """ Test whether new meeup is created if data provided """

        new_meetup = self.create_meetup()

        self.assertEqual(new_meetup.status_code, 201)
        self.assertTrue(new_meetup.json["data"])

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

        self.assertEqual(self.fetch_upcoming_meetup(
            path="/api/v2/meetups/upcoming").status_code, 200)
        self.assertTrue(self.fetch_upcoming_meetup(
            path="/api/v2/meetups/upcoming").json["data"])
        self.assertNotEqual(self.fetch_upcoming_meetup(
            path="/api/v2/meetups/upcoming").status_code, 404)

    def tearDown(self):
        """ Destroys set up data before running each test """

        destroy_database()
        self.db.close()


if __name__ == "__main__":

    unittest.main()
