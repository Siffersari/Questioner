from datetime import datetime
from .base_model import BaseModels
from werkzeug.exceptions import BadRequest, NotFound


class QuestionModels(BaseModels):
    """ 
    This class QuestionModels contain all the 
    methods that interact with question details and
    record
    """

    def create_question(self, details):
        """ Creates a question to a meetup record """

        try:
            user = self.check_item_exists(
                "id", int(details["user"]), self.users)

            meetup = self.check_item_exists(
                "id", int(details["meetup"]), self.meetups)

        except KeyError as keyerror:
            raise BadRequest("{} is a required field".format(keyerror))

        if self.check_is_error(user):
            raise NotFound("User not found")

        if self.check_is_error(meetup):
            raise NotFound("Meetup not found")

        if self.check_is_error(self.check_missing_details(details)):
            raise BadRequest(self.check_missing_details(details))

        question = {
            "id": len(self.questions) + 1,
            "createdOn": datetime.now(),
            "createdBy": user[0]["id"],
            "meetup": meetup[0]["id"],
            "title": details["title"],
            "body": details["body"],
            "votes": 0
        }

        self.questions.append(question)

        return self.makeresp(
            {
                "user": question["id"],
                "meetup": question["meetup"],
                "title": question["title"],
                "body": question["body"]
            }, 201)

    def upvote_question(self, question_id):
        """ 
        Increases the number of votes of a specific 
        question by 1 
        """

        data = self.check_question_exists(question_id)

        if type(data) == str:
            raise NotFound("Question not found")

        self.questions[data[0][0]
                       ]["votes"] = self.questions[data[0][0]]["votes"] + 1

        return self.makequestionresponse(data)

    def downvote_question(self, question_id):
        """ 
        Decreases the number of votes of a specific 
        question by 1 
        """

        question = self.check_question_exists(question_id)

        if self.check_is_error(question):
            return self.makeresp("Question not found", 404)

        self.questions[question[0][0]
                       ]["votes"] = self.questions[question[0][0]]["votes"] - 1

        return self.makequestionresponse(self.check_question_exists(question_id))

    def check_question_exists(self, question_id):
        """ 
        This method takes in a question id and checks if the
        question id exists in the questions database
        """
        question = self.check_item_return_index(
            "id", question_id, self.questions)

        return question

    def makequestionresponse(self, question):
        """
        This method takes in data and selects what part of 
        data to make response with and responds
        """

        resp = {
            "meetup": question[0][1]["meetup"],
            "title": question[0][1]["title"],
            "body": question[0][1]["body"],
            "votes": question[0][1]["votes"]
        }

        return self.makeresp(resp, 200)
