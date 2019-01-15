from .base_model import BaseModels
from werkzeug.exceptions import BadRequest, NotFound


class RsvpModels(BaseModels):
    """
    This class RsvpModels contains all the methods that
    are used to manipulated rsvps of a specific meetup
    """

    def respond_meetup(self, details, meetup_id):
        """ Responds to a meetup RSVP """

        error = self.check_missing_details(details)

        if self.check_is_error(error):
            raise BadRequest(error)

        try:
            user = self.check_item_exists(
                "id", int(details["user"]), self.users)
            response = details["response"]
        except KeyError as error:
            return self.makeresp("{} is a required data field".format(error), 400)

        meetup = self.check_item_exists(
            "id", meetup_id, self.meetups)

        if self.check_is_error(user):
            return self.makeresp("User not found", 404)

        if self.check_is_error(meetup):
            return self.makeresp("This Meetup is not found", 404)

        validresp = ["yes", "Yes", "YES", "no", "No", "NO","maybe", "Maybe"]

        if response not in validresp:
            return self.makeresp("Your answer may only take one of the form {}".format(validresp), 400)

        rsvp = {
            "id": len(self.rsvps) + 1,
            "meetup": meetup[0]["id"],
            "user": user[0]["id"],
            "response": response
        }

        self.rsvps.append(rsvp)

        resp = {
            "id": rsvp["id"],
            "meetup": rsvp["meetup"],
            "topic": meetup[0]["topic"],
            "status": rsvp["response"]
        }

        return self.makeresp(resp, 201)

        
