import unittest
import json
import os
from ... import create_app
from ... db_con import create_tables, destroy_database


class TestQuestions(unittest.TestCase):
    """
    Contains testcases for questions 
    for a meetup record
    """

    def setUp(self):
        """ Sets up what the test will need before it runs """

        self.app = create_app("testing")

        self.client = self.app.test_client()

        os.environ["DATABASE_URL"] = os.getenv("DATABASE_TESTING_URL")

        create_tables()

        self.data = {
            "firstname": "User",
            "lastname": "Test",
            "othername": "UserTest",
            "email": "test@test.com",
            "phoneNumber": "0712332112",
            "username": "testuser",
            "password": "P@5sword"
        }

        self.meetup = {
            "location": "Angle House, Nairobi",
            "images": ["img1.jgp", "img2.jpg"],
            "topic": "Do It Yourself",
            "happeningOn": "Feb 4 2019 10:30AM",
            "tags": ["Creative", "Technology"],
            "user": 1
        }

        self.question = {
            "user": 1,
            "meetup": 1,
            "title": "Leather bag price",
            "body": "How much would a good leather bag cost"

        }

        self.votedetail = {
            "user": 1
        }

        self.content_type = "application/json"

        self.user = self.client.post("/api/v2/auth/signup",
                                     data=json.dumps(self.data), content_type="application/json")

        login = self.login_user()

        self.assertEqual(login.status_code, 200)

        self.assertTrue(self.login_user().json["data"][0]["token"])

        self.headers = {'Authorization': 'Bearer {}'.format(
            login.json["data"][0]["token"])}

        self.create_meetup()

    def login_user(self, path="/api/v2/auth/login", data={}):
        """ Logs in a user if registered """

        if not data:
            data = self.data

        response = self.client.post(path, data=json.dumps(
            data), content_type="application/json")

        return response

    def create_meetup(self, path="api/v2/meetups", data={}):
        """ Creates a meetup """

        if not data:
            data = self.meetup

        response = self.client.post(path, data=json.dumps(
            data), content_type=self.content_type, headers=self.headers)

        return response

    def post_question(self, path="/api/v2/questions", data={}):
        """ Creates a question for a specific meetup """

        if not data:
            data = self.question

        response = self.client.post(path, data=json.dumps(
            data), content_type="application/json", headers=self.headers)

        return response

    def fetch_specific_question(self, path="/api/v2/questions/<int:question-i>"):
        """ Gets a specific question record using the question id """

        response = self.client.get(path, headers=self.headers)

        return response

    def create_comment(self, path="/api/v2/comments", data={}):
        """ Posts a comment to a question """

        if not data:
            data = {
                "user": 1,
                "question": 1,
                "comment": "Just a sample comment"
            }

        response = self.client.post(path, data=json.dumps(
            data), content_type=self.content_type, headers=self.headers)

        return response

    def upvote_question(self, path="/api/v2/questions/<int:question_id>/upvote", data={}):
        """ Increases votes of a specific question by 1 """

        response = self.client.patch(path, data=json.dumps(
            self.votedetail), content_type=self.content_type, headers=self.headers)

        return response

    def downvote_question(self, path="/api/v2/questions/<int:question_id>/downvote", data={}):
        """ Downvotes a question to a specific meetup """

        response = self.client.patch(path, data=json.dumps(
            self.votedetail), content_type=self.content_type, headers=self.headers)

        return response

    def test_post_new_question(self):
        """ Tests whether new question is created with data provided """

        new_question = self.post_question()

        self.assertEqual(new_question.status_code, 201)
        self.assertTrue(new_question.json["data"])

    def test_fetch_specific_question(self):
        """ Tests for successfull fetch of question if correct id """

        new_question = self.post_question()

        self.assertEqual(new_question.status_code, 201)

        self.assertEqual(self.fetch_specific_question(
            path="/api/v2/questions/1").status_code, 200)

        self.assertTrue(self.fetch_specific_question(
            path="/api/v2/questions/1").json["data"][0]["title"])

        self.assertTrue(self.fetch_specific_question(
            path="/api/v2/questions/1").json["data"][0]["body"])

    def test_fails_to_fetch_returning_error_if_missing_id(self):
        """ Tests for failure if nonexistent question id provided """

        self.assertEqual(self.fetch_specific_question(
            path="/api/v2/questions/1").status_code, 404)

        self.assertTrue(self.fetch_specific_question(
            path="/api/v2/questions/1").json["error"])

    def test_create_comment(self):
        """ Tests whether new question is created with data provided """

        new_question = self.post_question()

        self.assertEqual(new_question.status_code, 201)

        self.assertEqual(self.create_comment().status_code, 201)

        self.assertTrue(self.create_comment().json["data"])

    def test_upvote_question(self):
        """ Tests for upvoting a question """

        new_vote = self.post_question()
        self.assertEqual(new_vote.status_code, 201)

        vote = self.upvote_question(
            path="/api/v2/questions/{}/upvote".format(new_vote.json["data"][0]["id"]))

        self.assertEqual(vote.status_code, 200)

        self.assertTrue(self.upvote_question(path="/api/v2/questions/{}/upvote".format(
            new_vote.json["data"][0]["user"])).json["data"][0]["votes"])
        self.assertEqual(self.upvote_question(path="/api/v2/questions/{}/upvote".format(
            new_vote.json["data"][0]["user"])).json["data"][0]["votes"], 3)

    def test_downvote_question(self):
        """ Tests for downvoting a question """
        new_vote = self.post_question()
        self.assertEqual(new_vote.status_code, 201)

        vote = self.downvote_question(
            path="/api/v2/questions/{}/upvote".format(new_vote.json["data"][0]["id"]))

        self.assertEqual(vote.status_code, 200)

    def tearDown(self):
        """ Destroys set up data before running each test """

        destroy_database()

    os.environ["DATABASE_URL"] = "dbname='questioner' host='localhost' port='5432' user='leewel' password='root'"


if __name__ == "__main__":

    unittest.main()
