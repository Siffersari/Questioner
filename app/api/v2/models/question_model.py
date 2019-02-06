from datetime import datetime
from .base_model import BaseModels
from .meetup_model import check_meetup_exists
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

            meetup = self.sql.fetch_details_by_criteria(
                "meetup_id", self.question_details["meetup"], "meetups")

            existing = self.sql.fetch_details_if_text_exists(
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

            if [meet_id[1] for meet_id in existing if self.question_details["meetup"] in meet_id]:

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

        locations, vote_id = ["question_id", "user_id", "meetup_id", "vote"], ''

        question = self.sql.fetch_details_by_criteria(
            "question_id", question_id, "questions")

        votes = self.sql.fetch_details_by_criteria(
            "question_id", question_id, "votes")

        if not question:
            return self.makeresp("Question not found", 404)

        isempty = DataValidators(
            self.question_details).check_values_not_empty()

        if isinstance(isempty, str):
            return self.makeresp(isempty, 400)

        user_id = self.question_details["user"]

        try:
            user = SqlHelper().fetch_details_by_criteria(
                "user_id", user_id, "users")

        except KeyError as errs:
            return self.makeresp("{} is a required key".format(errs), 400)

        if not user:
            return self.makeresp("User does not exist. Please register first", 404)

        voted_users = [
            user for user in votes if self.question_details["user"] in user]

        if voted_users:

            vote_id = voted_users[0][0]

            if [vote[3] for vote in voted_users if "up" in vote]:

                return self.makeresp("You have already upvoted this question", 403)

            else:

                self.sql.update_votes(vote_id, "up")

        elif not voted_users:

            details = {
                "question": question_id,
                "user": self.question_details["user"],
                "vote": "up",
                "meetup": question[0][1]
            }

            vote_id = SqlHelper(details).save_to_database(locations, "votes")

        data = self.sql.vote_question(question_id)

        return self.makequestionresponse(data, vote_id)

    def downvote_question(self, question_id):
        """ 
        Decreases the number of votes by 1 
        """
        locations, vote_id = ["question_id", "user_id", "meetup_id", "vote"], ''

        question = self.sql.fetch_details_by_criteria(
            "question_id", question_id, "questions")

        votes = self.sql.fetch_details_by_criteria(
            "question_id", question_id, "votes")

        if not question:
            return self.makeresp("Question not found", 404)

        isempty = DataValidators(
            self.question_details).check_values_not_empty()

        if isinstance(isempty, str):
            return self.makeresp(isempty, 400)

        try:
            user = self.sql.fetch_details_by_criteria(
                "user_id", self.question_details["user"], "users")

        except KeyError as keyerr:
            return self.makeresp("{} is a required key".format(keyerr), 400)

        if not user:
            return self.makeresp("User does not exist. Please register first", 404)

        voted_users = [
            user for user in votes if self.question_details["user"] in user]

        if voted_users:

            vote_id = voted_users[0][0]

            if [vote[3] for vote in voted_users if "down" in vote]:

                return self.makeresp("You have already downvoted this question", 403)

            else:

                self.sql.update_votes(vote_id, "down")

        elif not voted_users:

            details = {
                "question": question_id,
                "user": self.question_details["user"],
                "vote": "down",
                "meetup": question[0][1]
            }

            vote_id = SqlHelper(details).save_to_database(locations, "votes")

        data = self.sql.vote_question(question_id, "down")

        return self.makequestionresponse(data, vote_id)

    def makequestionresponse(self, question, vote_id=''):
        """
        This method takes in data and selects what part of 
        data to make response with and responds
        """

        resp = {
            "meetup": question[0],
            "title": question[1],
            "body": question[2],
            "votes": question[3],
            "id": vote_id
        }

        return self.makeresp(resp, 200)

    def fetch_specific_question(self, question_id):
        """ 
        This methods takes in a question id and checks
        if the question exists then returns it 
        """

        question = self.sql.fetch_details_by_criteria(
            "question_id", question_id, "questions")

        response, status = "", 200

        if not question:

            return self.makeresp("Question not found", 404)

        user = self.sql.get_username_by_id(int(question[0][2]))

        response = self.makeresp({

            "user": user[0],
            "meetup": question[0][1],
            "title": question[0][3],
            "body": question[0][4],
            "createdOn": question[0][6],
            "votes": question[0][5]
        }, status)

        return response

    def fetch_all_questions(self):
        """ 
        Returns all questions 
        """

        response = []

        questions = self.sql.get_all("questions")

        for items in questions:

            user = self.sql.get_username_by_id(items[2])[0]

            meetup = check_meetup_exists(items[1])

            response.append({
                "id": items[0],
                "createdBy": user,
                "meetup": items[1],
                "meetupTopic": meetup[0][2],
                "title": items[3],
                "body": items[4],
                "createdOn": items[6],
                "votes": items[5]

            })

        return self.makeresp(response, 200)

    def delete_question(self, question_id):
        """ Deletes from the database a question """

        question = self.sql.fetch_details_by_criteria(
            "question_id", question_id, "questions")

        if not question:

            return self.makeresp("This question could not be found", 404)

        if not self.question_details["user"] == question[0][2]:

            return self.makeresp("You can not delete a question you don't own", 403)

        SqlHelper().delete_from_database(question_id, "questions")

        SqlHelper().delete_from_database(question_id, "comments", "question_id")

        SqlHelper().delete_from_database(question_id, "votes", "question_id")

        return self.makeresp({"message": "This question has been deleted successfully"}, 200)
