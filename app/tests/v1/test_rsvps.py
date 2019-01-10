import unittest
import json
from ... import create_app


class TestRsvps(unittest.TestCase):
    """ 
    Contains testcases for RSVPs to for a meetup
    record
    """

    def setUp(self):
        """ Setsup what the test will require """

        self.app = create_app()

        self.client = self.app.test_client()

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

        self.user = self.client.post(
            "/api/v1/auth/signup", data=json.dumps(self.data), content_type="application/json")
        self.assertEqual(self.user.status_code, 201)

        self.meetup = self.client.post(
            "/api/v1/meetups", data=json.dumps(self.meetup), content_type="application/json")
        self.assertEqual(self.meetup.status_code, 201)

        self.rsvp = {
            "user": self.user.json["data"][0]["id"],
            "meetup": self.meetup.json["data"][0]["id"],
            "response": "yes"
        }

    def respond_meetup(self, path="/api/v1/meetups/<int:meetup_id>/rsvps", data={}):
        """ Responds to meetup RSVP """

        if not data:
            data = self.rsvp

        response = self.client.post(path, data=json.dumps(
            data), content_type="application/json")

        return response

    def test_respond_meetup(self):
        """ Tests for responding to a meetup """

        new_rsvp = self.respond_meetup(path="/api/v1/meetups/{}/rsvps".format(self.rsvp["meetup"]))

        self.assertEqual(new_rsvp.status_code, 201)
        self.assertTrue(new_rsvp.json["data"])
