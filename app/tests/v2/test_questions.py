import unittest
import json
from ... import create_app
from ... db_con import init_test_db, destroy_database


class TestQuestions(unittest.TestCase):
    """
    Contains testcases for questions 
    for a meetup record
    """

    def setUp(self):
        """ Sets up what the test will need before it runs """

        self.app = create_app("testing")

        self.client = self.app.test_client()

        self.db = init_test_db()

        self.data = {
            "firstname": "Mohammed",
            "lastname": "Mohali",
            "othername": "Mrali",
            "email": "ali@moh.com",
            "phoneNumber": "0707070707",
            "username": "Mohali",
            "password": "P@5sword"
        }

        self.meetup = {
            "location": "House of Leather, Nairobi",
            "images": ["img1.jgp", "img2.jpg"],
            "topic": "All the Leather you can get",
            "happeningOn": "Mar 8 2019 11:30AM",
            "tags": ["Creative", "Leather"],
            "username": "Leewel"
        }

    def upvote_question(self, path="/api/v2/questions/<int:question_id>/upvote", data={}):
        """ Increases votes of a specific question by 1 """

        response = self.client.patch(path)

        return response

    def downvote_question(self, path="/api/v2/questions/<int:question_id>/downvote", data={}):
        """ Downvotes a question to a specific meetup """

        response = self.client.patch(path)

        return response

    def test_post_new_question(self):
        """ Tests whether new question is created with data provided """
        pass

    def tearDown(self):
        """ Destroys set up data before running each test """

        destroy_database()
        self.db.close()


if __name__ == "__main__":

    unittest.main()
