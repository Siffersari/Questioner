from .common_model import CommonModels
from .meetup_model import meetups
from .user_model import users

# This array, rsvps, stores all rsvps to meetups on the platfrom

rsvps = []


class RsvpModels(CommonModels):
    """
    This class RsvpModels contains all the methods that
    are used to manipulated rsvps of a specific meetup
    """

    def __init__(self):
        self.db = rsvps

    def respond_meetup(self, details, meetup_id):
        """ Responds to a meetup RSVP """

        user = [user for user in users if user["id"] == int(details["user"])]

        meetup = [meetup for meetup in meetups if meetup["id"] == int(meetup_id)]

        if not user:
            return self.makeresp("User not found", 404)

        if not meetup:
            return self.makeresp("This Meetup is not found", 404)

        rsvp = {
            "id": len(self.db) + 1,
            "meetup": meetup[0]["id"],
            "user": user[0]["id"],
            "response": details["response"]
        }

        self.db.append(rsvp)

        resp = {
            "id": rsvp["id"],
            "meetup": rsvp["meetup"],
            "topic": meetup[0]["topic"],
            "status": rsvp["response"]
        }

        return self.makeresp(resp, 201)