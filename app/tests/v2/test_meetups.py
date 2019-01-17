import unittest
import json
from ... import create_app
from ... db_con import init_test_db, destroy_database


class TestMeetups(unittest.TestCase):
    """
    Contains test cases for the meetups
    """

    def setUp(self):
        """ Sets up what the test will need before it runs """

        self.app = create_app()

        self.client = self.app.test_client()

        self.db = init_test_db()

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

        pass

 


    def tearDown(self):
        """ Destroys set up data before running each test """

        destroy_database()
        self.db.close()


if __name__ == "__main__":

    unittest.main()
