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
            "Tags": ["Creative", "Technology"],
            "username": "Leewel",

        }

    def create_meetup(self, path="api/v1/meetups", data={}):
        """ Creates a meetup """
        if not data:
            data = self.data

        response = self.client.post(path, data=json.dumps(data), content_type="application/json")
        
        return response

    def test_create_new_meetup(self):
        """ Test whether new meeup is created if data provided """

        new_meetup = self.create_meetup()

        self.assertEqual(new_meetup.status_code, 201)
        self.assertTrue(new_meetup.json["data"])



    def tearDown(self):
        """ Destroy app and variable instances """
        self.app = None



if __name__ == "__main__":
    unittest.main()