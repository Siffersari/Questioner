from datetime import datetime
from .base_model import BaseModels
from ..utils.validators import DataValidators
from ..utils.sql_helpers import SqlHelper
from flask import current_app
from ....db_con import create_tables


class QuestionModels(BaseModels):
    """ 
    This class QuestionModels contain all the 
    methods that interact with question details and
    record
    """

    def __init__(self, details={}):
        self.question_details = details
        self.db = create_tables()
        self.sql = SqlHelper()

    def create_question(self):
        """ Creates a question to a meetup record """

        locations = ["meetup_id", "user_id", "title", "body"]

        try:

            user = self.sql.get_username_by_id(
                int(self.question_details["user"]))

            meetup = self.sql.fetch_details_by_id(
                "meetup_id", self.question_details["meetup"], "meetups")

            existing = self.sql.fetch_id_if_text_exists(
                "title", self.question_details["title"], "questions")

            title = self.question_details["title"]

            body = self.question_details["body"]

        except KeyError as keyerror:
            return self.makeresp("{} is a required field".format(keyerror), 400)

        isempty = DataValidators(
            self.question_details).check_values_not_empty()

        if isinstance(isempty, str):
            return self.makeresp(isempty, 400)

        if not user:
            return self.makeresp("User not found", 404)

        if not meetup:
            return self.makeresp("Meetup not found", 404)

        if not self.check_is_error(existing):
            return self.makeresp("This Question already exists", 409)

        question = {
            "meetup": self.question_details["meetup"],
            "createdBy": self.question_details["user"],
            "title": title,
            "body": body
        }

        question_id = SqlHelper(question).save_to_database(
            locations, "questions")

        return self.makeresp(
            {
                "id": question_id,
                "user": question["createdBy"],
                "meetup": question["meetup"],
                "title": question["title"],
                "body": question["body"]
            }, 201)

    def upvote_question(self, question_id):
        """ 
        Increases the number of votes of a specific 
        question by 1 
        """

        question = self.sql.fetch_details_by_id(
            "question_id", question_id, "questions")

        if not question:
            return self.makeresp("Question not found", 404)

        isempty = DataValidators(
            self.question_details).check_values_not_empty()

        if isinstance(isempty, str):
            return self.makeresp(isempty, 400)

        user_id = self.question_details["user"]

        try:
            user = SqlHelper().fetch_details_by_id(
                "user_id", user_id, "users")

        except KeyError as errs:
            return self.makeresp("{} is a required key".format(errs), 400)

        if not user:
            return self.makeresp("User does not exist. Please register first", 404)

        data = self.sql.vote_question(question_id)

        return self.makequestionresponse(data)

    def downvote_question(self, question_id):
        """ 
        Decreases the number of votes by 1 
        """

        question = self.sql.fetch_details_by_id(
            "question_id", question_id, "questions")

        if not question:
            return self.makeresp("Question not found", 404)

        isempty = DataValidators(
            self.question_details).check_values_not_empty()

        if isinstance(isempty, str):
            return self.makeresp(isempty, 400)

        try:
            user = self.sql.fetch_details_by_id(
                "user_id", self.question_details["user"], "users")

        except KeyError as keyerr:
            return self.makeresp("{} is a required key".format(keyerr), 400)

        if not user:
            return self.makeresp("User does not exist. Please register first", 404)

        data = self.sql.vote_question(question_id, "down")

        return self.makequestionresponse(data)

    def post_comment(self):
        """ Posts a comment to a question """

        locations = ["question_id", "user_id", "comments"]

        try:

            user = self.sql.get_username_by_id(
                int(self.question_details["user"]))

            question = self.sql.fetch_details_by_id(
                "question_id", self.question_details["question"], "questions")

            comment = self.question_details["comment"]

            isempty = DataValidators(
                self.question_details).check_values_not_empty()

            if isinstance(isempty, str):
                return self.makeresp(isempty, 400)

            if isinstance(comment, str):
                self.question_details["comment"] = [comment]

        except KeyError as keyerror:
            return self.makeresp("{} is a required field".format(keyerror), 400)

        if not user:
            return self.makeresp("User not found", 404)

        if not question:
            return self.makeresp("Question not found", 404)

        comment_id = SqlHelper(self.question_details).save_to_database(
            locations, "comments")

        return self.makeresp(
            {
                "id": comment_id,
                "user": user[0],
                "question": question[0],
                "title": question[3],
                "body": question[4],
                "comment": comment
            }, 201)

    def makequestionresponse(self, question):
        """
        This method takes in data and selects what part of 
        data to make response with and responds
        """

        resp = {
            "meetup": question[0],
            "title": question[1],
            "body": question[2],
            "votes": question[3]
        }

        return self.makeresp(resp, 200)

    def fetch_specific_question(self, question_id):
        """ 
        This methods takes in a question id and checks
        if the question exists then returns it 
        """

        question = self.sql.fetch_details_by_id(
            "question_id", question_id, "questions")

        response, status = "", 200

        if not question:

            return self.makeresp("Question not found", 404)

        user = self.sql.get_username_by_id(int(question[1]))

        response = self.makeresp({

            "user": user[0],
            "meetup": question[2],
            "title": question[3],
            "body": question[4]
        }, status)

        return response

    def fetch_all_questions(self):
        """ 
        Returns all questions 
        """

        response = []

        questions = self.sql.get_all("questions")

        for items in questions:

            user = self.sql.get_username_by_id(items[1])[0]

            response.append({
                "id": questions[0][0],
                "createdBy": user,
                "meetup": items[2],
                "topic": items[3],
                "body": items[4],
                "createdOn": items[6]

            })

        return self.makeresp(response, 200)

    def fetch_all_comments(self):
        """ Fetches all comments to questions """

        response = []

        comments = self.sql.get_all("comments")

        for items in comments:

            user = self.sql.get_username_by_id(items[2])[0]

            response.append({
                "id": items[0],
                "createdBy": user,
                "question": items[1],
                "comment": items[3],
                "createdOn": items[4]

            })

        return self.makeresp(response, 200)

    def fetch_one_comment(self, comment_id):
        """ Gets just one comment record with the passed id """

        comment_data = ''

        comment = self.sql.fetch_details_by_id(
            "comment_id", comment_id, "comments")

        if not comment:

            return self.makeresp("This comment cannot not be found", 404)

        user = self.sql.get_username_by_id(int(comment[2]))

        if len(comment[3]) == 1:

            comment_data = comment[3][0]

        response = self.makeresp({

            "user": user[0],
            "question": comment[1],
            "comment": comment_data,
            "createdOn": comment[4]
        }, 200)

        return response

    def delete_question(self, question_id):
        """ Deletes from the database a question """

        question = self.sql.fetch_details_by_id(
            "question_id", question_id, "questions")

        if not question:

            return self.makeresp("This question could not be found", 404)

        if not self.question_details["user"] == question[1]:

            return self.makeresp("You can not delete a question you don't own", 403)

        SqlHelper().delete_from_database(question_id, "questions")

        return self.makeresp({"message": "This question has been deleted successfully"}, 200)

    def remove_comment(self, comment_id):
        """ Removes a comment from the database """

        comment = self.sql.fetch_details_by_id(
            "comment_id", comment_id, "comments")

        if not comment:

            return self.makeresp("This comment could not be found", 404)

        if not self.question_details["user"] == comment[1]:

            return self.makeresp("You can not delete a comment you don't own", 403)

        SqlHelper().delete_from_database(comment_id, "comments")

        return self.makeresp({"message": "Comment deleted successfully"}, 200)
