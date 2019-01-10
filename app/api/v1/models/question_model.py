from datetime import datetime
from .common_model import CommonModels

# This array questions, stores all question
# To a specific meetup


class QuestionModels(CommonModels):
    """ 
    This class QuestionModels contain all the 
    methods that interact with question details and
    record
    """

    def create_question(self, details):
        """ Creates a question to a meetup record """

        try:            
            user = self.check_item_exists("id", int(details["user"]), self.users)

            meetup = self.check_item_exists(
                "id", int(details["meetup"]), self.meetups)

        except Exception as keyerror:
            return self.makeresp("{} is a required field".format(keyerror), 400)

        if self.check_is_error(user):
            return self.makeresp("User not found", 404)

        if self.check_is_error(meetup):
            return self.makeresp("Meetup not found", 404)

        if self.check_is_error(self.check_missing_details(details)):
            return self.makeresp(self.check_missing_details(details), 400)

        

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

        resp = {
            "user": question["id"],
            "meetup": question["meetup"],
            "title": question["title"],
            "body": question["body"]
        }

        return self.makeresp(resp, 201)

        

        

    def upvote_question(self, question_id):
        """ 
        Increases the number of votes of a specific 
        question by 1 
        """

        data = self.check_question_exists(question_id)

        if type(data) == str:
            return self.makeresp("Question not found", 404)

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
                       
        return self.makequestionresponse(question)

        

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

