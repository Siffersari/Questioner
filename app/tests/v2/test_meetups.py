import unittest
from .base_test import BaseTest


class TestMeetups(BaseTest):
    """ Contains all tests for meetup cases """

    def setUp(self):
        """ Sets up what the test will need before it runs """

        BaseTest.setUp(self)

    def test_create_new_meetup(self):
        """ Test cases for creating  a new meetup """

        new_meetup = self.create_meetup()

        self.assertEqual(new_meetup.status_code, 201)

    def test_raises_badrequest_if_required_missing(self):
        """ 
        Test for Badrequest when a required field is missing
        """

        missing_topic = self.create_meetup(data=self.missing_meetup_data)

        self.assertEqual(missing_topic.status_code, 400)
        self.assertTrue(missing_topic.json["error"])

    def test_creates_meetup_if_missing_images_key(self):
        """ 
        Test whether new meetup is created if images key
        are not provided 
        """

        missing_images = self.create_meetup(data=self.imageless_meetup_data)

        self.assertEqual(missing_images.status_code, 201)
        self.assertTrue(missing_images.json["data"])

    def test_fetches_correct_meetup_id_if_correct_details(self):
        """
        Tests whether the correct meetup id is fetched if the
        correct details are provided 
        """

        meetup = self.create_meetup()

        self.assertEqual(meetup.status_code, 201)
        self.assertTrue(meetup.json["data"])

        self.assertEqual(self.fetch_meetup_id(path="/api/v2/meetups/{}/{}".format(
            self.meetup_data["topic"], self.meetup_data["location"])).status_code, 200)

        self.assertTrue(self.fetch_meetup_id(path="/api/v2/meetups/{}/{}".format(
            self.meetup_data["topic"], self.meetup_data["location"])).json["data"][0]["id"] == 1)

    def test_failure_if_non_existent_meetup(self):
        """
        Tests for failure if no meetup exists at all 
        """

        self.assertEqual(self.fetch_meetup_id(path="/api/v2/meetups/{}/{}".format(
            self.meetup_data["topic"], self.meetup_data["location"])).status_code, 404)

        self.assertTrue("No meetup" in self.fetch_meetup_id(path="/api/v2/meetups/{}/{}".format(
            self.meetup_data["topic"], self.meetup_data["location"])).json["error"])

    def test_failure_if_wrong_topic(self):
        """ 
        Test for error if provide meetup topic doesn't
        exist 
        """

        meetup = self.create_meetup()

        self.assertEqual(meetup.status_code, 201)
        self.assertTrue(meetup.json["data"])

        self.assertEqual(self.fetch_meetup_id(path="/api/v2/meetups/{}/{}".format(
            self.wrong_meet_topic["topic"], self.wrong_meet_topic["location"])).status_code, 404)

        self.assertTrue("No meetup" in self.fetch_meetup_id(path="/api/v2/meetups/{}/{}".format(
            self.wrong_meet_topic["topic"], self.wrong_meet_topic["location"])).json["error"])

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

        self.assertEqual(self.post_images(
            path="/api/v2/meetups/1/images").status_code, 404)

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

        self.assertEqual(self.add_tags(
            path="/api/v2/meetups/1/tags").status_code, 404)

    def test_fetches_meetup_questions(self):
        """ Tests for successful fetch of meetup questions """
        
        self.create_meetup()

        self.post_question()

        self.assertEqual(self.fetch_meetup_questions(path="/api/v2/meetups/1/questions").json["data"][0]["id"], 1)

    def tearDown(self):
        """ Destroys set up data before running each test """

        BaseTest.tearDown(self)


if __name__ == "__main__":

    unittest.main()
