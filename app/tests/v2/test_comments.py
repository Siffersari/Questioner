import unittest
from .base_test import BaseTest


class TestComments(BaseTest):

    """
    Contains test cases for comments
    to question records 
    """

    def setUp(self):
        """ Set up pre-requisites to the test runs """

        BaseTest.setUp(self)

        self.create_meetup(data=self.meetup_data_2)

        self.new_question = self.post_question()

        self.new_comment = self.create_comment()

    def test_create_comment(self):
        """ Tests whether new question is created with data provided """

        self.assertEqual(self.new_question.status_code, 201)

        self.assertEqual(self.new_comment.status_code, 201)

        self.assertTrue(self.new_comment.json["data"])

    def test_fetch_comments(self):
        """ Tests for successfull fetch of comments """

        self.assertEqual(self.new_question.status_code, 201)

        self.assertEqual(self.new_comment.status_code, 201)

        self.assertTrue(self.new_comment.json["data"][0]["comment"])

        self.assertEqual(self.fetch_all_comments(
            path="/api/v2/questions/1/comments").status_code, 200)

        self.assertTrue(self.fetch_all_comments(
            path="/api/v2/questions/1/comments").json["data"][0]["comment"])

        self.assertEqual(self.new_comment.json["data"][0]["comment"], self.fetch_all_comments(path="/api/v2/questions/1/comments").json["data"][0]["comment"][0])

    def test_fetch_one_comment(self):
        """ Tests for success when fetching comment with existing id """

        self.assertEqual(self.new_question.status_code, 201)

        self.assertEqual(self.new_comment.status_code, 201)

        self.assertTrue(self.new_comment.json["data"][0]["comment"])

        self.assertEqual(self.fetch_one_comment(
            path="/api/v2/comments/1").status_code, 200)

        self.assertTrue(self.fetch_one_comment(
            path="/api/v2/comments/1").json["data"][0]["comment"])

        self.assertEqual(self.new_comment.json["data"][0]["comment"], self.fetch_one_comment(path="/api/v2/comments/1").json["data"][0]["comment"])

    def test_delete_comment_if_owner_success(self):
        """ Test for successful delete of comment by owner """

        self.assertEqual(self.new_question.status_code, 201)

        self.assertEqual(self.new_comment.status_code, 201)

        self.assertEqual(self.delete_comment(
            path="/api/v2/comments/1").status_code, 200)

        self.assertEqual(self.delete_comment(
            path="/api/v2/comments/1").status_code, 404)

    def tearDown(self):
        """ Destroys set up data before running each test """

        BaseTest.tearDown(self)


if __name__ == "__main__":

    unittest.main()
