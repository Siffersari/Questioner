import unittest
import json
from ... import create_app
from ... db_con import init_test_db, destroy_database


class TestRsvps(unittest.TestCase):
    """ 
    Contains testcases for RSVPs to for a meetup
    record
    """

    def setUp(self):
        """ Setsup what the test will require """

        self.app = create_app("testing")

        self.client = self.app.test_client()

        self.db = init_test_db()

        self.data = {
            "firstname": "Wayne",
            "lastname": "Rooney",
            "othername": "Plays",
            "email": "Wayne@roon.com",
            "phoneNumber": "0707070707",
            "username": "wayneroon",
            "password": "P@5sword"
        }

        self.meetup = {
            "location": "Kiwanjani, Nairobi",
            "images": ["img1.jgp", "img2.jpg"],
            "topic": "Ligi ndoge",
            "happeningOn": "Mar 2 2019 11:30AM",
            "tags": ["Football", "Sports"],
            "username": "Janet"
        }



    def test_respond_meetup(self):
        """ Tests for responding to a meetup """

        pass

    def tearDown(self):
        """ Destroys set up data before running each test """

        destroy_database()
        self.db.close()


if __name__ == "__main__":

    unittest.main()
