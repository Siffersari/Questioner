import unittest
import json
import os
from ... import create_app
from ... db_con import create_tables, destroy_database
from .data import Data


class BaseTest(unittest.TestCase):
    """
    This class BaseTest, contains setup used by 
    all other tests
    """

    def setUp(self):
        """ Sets up what the test will need before it runs """

        self.app = create_app("testing")

        self.client = self.app.test_client()

        self.user_data = Data().test_user

        self.admin_data = Data().admin_data

        self.meetup_data = Data().meetup

        self.meetup_data_2 = Data().meetup2

        self.fetch_meet_data = Data().fetch_meetup_data

        self.wrong_meet_topic = Data().wrong_meet_topic

        self.missing_meetup_data = Data().missing_meetup_details

        self.imageless_meetup_data = Data().imageless_meetup_details

        self.question = Data().question

        self.comment_data = Data().comment

        self.image_data = Data().image

        self.tag_data = Data().tag

        self.rsvp = Data().rsvp

        os.environ["DATABASE_URL"] = os.getenv("DATABASE_TESTING_URL")

        create_tables()

        self.content_type = "application/json"

    def tearDown(self):
        """ Destroys set up data before running each test """

        destroy_database()

        os.environ["DATABASE_URL"] = "dbname='questioner' host='localhost' port='5432' user='leewel' password='root'"

    def get_token(self):

        login = self.login_user(role='admin')

        headers = {'Authorization': 'Bearer {}'.format(
            login.json["data"][0]["token"])}

        return headers

    def register_user(self, path="/api/v2/auth/signup", data={}):
        """ Registers a new user given data or default if not provided"""

        if not data:
            data = self.user_data

        response = self.client.post(path, data=json.dumps(
            data), content_type="application/json")

        return response

    def login_user(self, path="/api/v2/auth/login", data={}, role=''):
        """ Logs in a user if registered """

        if not data:
            data = self.user_data

        if role:

            data = self.admin_data 

        response = self.client.post(path, data=json.dumps(
            data), content_type="application/json")

        return response

    def logout_user(self, path="/api/v2/auth/logout"):
        """ Logs out a user """

        response = self.client.post(
            path, content_type=self.content_type, headers=self.get_token())

        return response

    def fetch_user_details(self, path="/api/v2/users"):
        """ Fetches details of a specific users """

        response = self.client.get(path, headers=self.get_token())

        return response

    def create_meetup(self, path="api/v2/meetups", data={}):
        """ Creates a meetup """

        if not data:
            data = self.meetup_data

        response = self.client.post(path, data=json.dumps(
            data), content_type=self.content_type, headers=self.get_token())

        return response

    def delete_meetup(self, path="api/v2/meetups/<meetup-id>"):
        """ Deletes a meetup """

        response = self.client.delete(
            path, content_type=self.content_type, headers=self.get_token())

        return response

    def post_images(self, path="api/v2/meetups/<meetup-id>/images", data={}):
        """ Adds images to meetup """

        if not data:
            data = self.image_data

        response = self.client.post(path, data=json.dumps(
            data), content_type=self.content_type, headers=self.get_token())

        return response

    def add_tags(self, path="api/v2/meetups/<meetup-id>/tags", data={}):
        """ Adds images to meetup """

        if not data:
            data = self.tag_data

        response = self.client.post(path, data=json.dumps(
            data), content_type=self.content_type, headers=self.get_token())

        return response

    def fetch_meetup_id(self, path="/api/v2/meetups/<topic>/<location>"):
        """ Fetches a specific meetup id given topic and location """

        response = self.client.get(
            path, headers=self.get_token())

        return response

    def fetch_specific_meetup(self, path="/api/v2/meetups/<meetup-id>"):
        """ Fetches a specific meetup record """

        response = self.client.get(path, headers=self.get_token())

        return response

    def fetch_upcoming_meetup(self, path="/api/v2/meetups/upcoming"):

        response = self.client.get(path)

        return response

    def post_question(self, path="/api/v2/questions", data={}):
        """ Creates a question for a specific meetup """

        if not data:
            data = self.question

        response = self.client.post(path, data=json.dumps(
            data), content_type="application/json", headers=self.get_token())

        return response

    def fetch_specific_question(self, path="/api/v2/questions/<int:question-i>"):
        """ Gets a specific question record using the question id """

        response = self.client.get(path, headers=self.get_token())

        return response

    def fetch_all_questions(self, path="/api/v2/questions"):
        """ Fetches all the questions posted """

        return self.client.get(path, headers=self.get_token())

    def fetch_meetup_questions(self, path="/api/v2/meetups/<meetup-id>/questions"):
        """ Fetches all the questions to a specific meetup record """

        return self.client.get(path, headers=self.get_token())

    def create_comment(self, path="/api/v2/comments", data={}):
        """ Posts a comment to a question """

        if not data:
            data = self.comment_data

        response = self.client.post(path, data=json.dumps(
            data), content_type=self.content_type, headers=self.get_token())

        return response

    def fetch_all_comments(self, path="/api/v2/questions/<int:question_id>/comments"):
        """ Fetches all the comments """

        return self.client.get(path, headers=self.get_token())

    def fetch_one_comment(self, path="/api/v2/comments/<int:comment-id>"):
        """ Gets just a single comment by the id """

        return self.client.get(path, headers=self.get_token())

    def upvote_question(self, path="/api/v2/questions/<int:question_id>/upvote"):
        """ Increases votes of a specific question by 1 """

        response = self.client.patch(
            path, content_type=self.content_type, headers=self.get_token())

        return response

    def downvote_question(self, path="/api/v2/questions/<int:question_id>/downvote"):
        """ Downvotes a question to a specific meetup """

        response = self.client.patch(
            path, content_type=self.content_type, headers=self.get_token())

        return response

    def delete_question(self, path="/api/v2/questions/<int:question_id>"):
        """ Deletes a specific question by ID """

        response = self.client.delete(
            path, content_type=self.content_type, headers=self.get_token())

        return response

    def delete_comment(self, path="/api/v2/comments/<int:comment_id>"):
        """ Deletes a specific comment by ID """

        response = self.client.delete(
            path, content_type=self.content_type, headers=self.get_token())

        return response

    def respond_meetup(self, path="/api/v2/meetups/<int:meetup_id>/rsvps", data={}):
        """ Responds to meetup RSVP """

        if not data:
            data = self.rsvp

        response = self.client.post(path, data=json.dumps(
            data), content_type="application/json", headers=self.get_token())

        return response
