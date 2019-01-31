import unittest
from .base_test import BaseTest


class TestRsvps(BaseTest):
    """
    Contains testcases for RSVPS 
    to a meetup record
    """

    def setUp(self):
        """ Sets up what the test will need before it runs """

        BaseTest.setUp(self)

        self.create_meetup()

    def test_respond_meetup(self):
        """ Tests for responding to a meetup """

        rsvp = self.respond_meetup(path="/api/v2/meetups/1/rsvps")

        self.assertEqual(rsvp.status_code, 201)

    def tearDown(self):
        """ Destroys set up data before running each test """

        BaseTest.tearDown(self)


if __name__ == "__main__":

    unittest.main()
