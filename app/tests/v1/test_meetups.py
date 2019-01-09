import unittest
import json
from ... import create_app


class TestMeetups(unittest.TestCase):
    """
    Contains test cases for the meetups
    """

    def setUp(self):
        """ Sets up what the test will need before it runs """

        self.app = create_app()

        self.client = self.app.test_client()

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

        self.valulessimage = {
            "location": "Angle House, Nairobi",
            "images": "",
            "topic": "No value Images",
            "happeningOn": "Feb 1 2019 10:30AM",
            "tags": ["Creative", "Technology"],
            "username": "Pogba",
        }

    def create_meetup(self, path="api/v1/meetups", data={}):
        """ Creates a meetup """
        if not data:
            data = self.data

        response = self.client.post(path, data=json.dumps(
            data), content_type="application/json")

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

    def tearDown(self):
        """ Destroy app and variable instances """
        self.app = None


if __name__ == "__main__":
    unittest.main()
