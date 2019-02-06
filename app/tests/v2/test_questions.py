import unittest
from .base_test import BaseTest


class TestQuestions(BaseTest):
    """
    Contains testcases for questions 
    for a meetup record
    """

    def setUp(self):
        """ Sets up what the test will need before it runs """

        BaseTest.setUp(self)

        self.create_meetup(data=self.meetup_data_2)

        self.new_question = self.post_question()

    def test_post_new_question(self):
        """ Tests whether new question is created with data provided """

        self.assertEqual(self.new_question.status_code, 201)
        self.assertTrue(self.new_question.json["data"])

    def test_fetch_all_questions(self):
        """ Tests that all questions are fetched successfully """

        self.assertEqual(self.new_question.status_code, 201)
        self.assertEqual(self.new_question.json["data"][0]["id"], 1)

    def test_fetch_specific_question(self):
        """ Tests for successfull fetch of question if correct id """

        self.assertEqual(self.new_question.status_code, 201)

        self.assertEqual(self.fetch_specific_question(
            path="/api/v2/questions/1").status_code, 200)

        self.assertTrue(self.fetch_specific_question(
            path="/api/v2/questions/1").json["data"][0]["title"])

        self.assertTrue(self.fetch_specific_question(
            path="/api/v2/questions/1").json["data"][0]["body"])

    def test_fails_to_fetch_returning_error_if_missing_id(self):
        """ Tests for failure if nonexistent question id provided """

        self.assertEqual(self.fetch_specific_question(
            path="/api/v2/questions/2").status_code, 404)

        self.assertTrue(self.fetch_specific_question(
            path="/api/v2/questions/2").json["error"])

    def test_upvote_question(self):
        """ Tests for upvoting a question """

        self.assertEqual(self.new_question.status_code, 201)

        vote = self.upvote_question(
            path="/api/v2/questions/{}/upvote".format(self.new_question.json["data"][0]["id"]))

        self.assertEqual(vote.status_code, 200)

        print(self.upvote_question(path="/api/v2/questions/{}/upvote".format(
            self.new_question.json["data"][0]["user"])).json)

        self.assertTrue(self.upvote_question(path="/api/v2/questions/{}/upvote".format(
            self.new_question.json["data"][0]["user"])).json["error"])

        self.assertEqual(self.upvote_question(path="/api/v2/questions/{}/upvote".format(
            self.new_question.json["data"][0]["user"])).json["error"], 'You have already upvoted this question')

    def test_downvote_question(self):
        """ Tests for downvoting a question """

        self.assertEqual(self.new_question.status_code, 201)

        vote = self.downvote_question(
            path="/api/v2/questions/{}/upvote".format(self.new_question.json["data"][0]["id"]))

        self.assertEqual(vote.status_code, 200)

    def test_delete_question_if_owner_success(self):
        """ Test for successful delete if the user is the owner of the question """

        self.assertEqual(self.new_question.status_code, 201)

        self.assertEqual(self.delete_question(
            path="/api/v2/questions/1").status_code, 200)

        self.assertEqual(self.delete_question(
            path="/api/v2/questions/1").status_code, 404)

    def tearDown(self):
        """ Destroys set up data before running each test """

        BaseTest.tearDown(self)


if __name__ == "__main__":

    unittest.main()
