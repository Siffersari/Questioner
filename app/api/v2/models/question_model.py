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
            "createdOn": datetime.now(),
            "createdBy": self.question_details["user"],
            "meetup": self.question_details["meetup"],
            "title": title,
            "body": body,
            "votes": 0
        }

        question_id = SqlHelper(question).save_question()

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

        try:
            user = self.sql.fetch_details_by_id(
                "user_id", self.question_details["user"], "users")

        except KeyError as keyerr:
            return self.makeresp("{} is a required key".format(keyerr), 400)

        if not user:
            return self.makeresp("User does not exist. Please register first", 404)

        data = SqlHelper(self.question_details).upvote_question(question_id)

        return self.makequestionresponse(data)

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
