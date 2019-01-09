from datetime import datetime
from .common_model import CommonModels
from .user_model import users
from .meetup_model import meetups

# This array questions, stores all question
# To a specific meetup

questions = []


class QuestionModels(CommonModels):
    """ 
    This class QuestionModels contain all the 
    methods that interact with question details and
    record
    """

    def __init__(self):
        self.db = questions

    def create_question(self, details):
        """ Creates a question to a meetup record """

        for item, data in details.items():
            if not data:
                return self.makeresp("{} is a required field".format(item), 400)

        user = [user for user in users if user["id"] == int(details["user"])]

        meetup = [meetup for meetup in meetups if meetup["id"]
                  == int(details["meetup"])]

        if not user:
            return self.makeresp("User not found", 404)

        if not meetup:
            return self.makeresp("Meetup not found", 404)

        question = {
            "id": len(self.db) + 1,
            "createdOn": datetime.now(),
            "createdBy": user[0]["id"],
            "meetup": meetup[0]["id"],
            "title": details["title"],
            "body": details["body"],
            "votes": 0
        }

        self.db.append(question)

        resp = {
            "user": question["id"],
            "meetup": question["meetup"],
            "title": question["title"],
            "body": question["body"]
        }

        return self.makeresp(resp, 201)