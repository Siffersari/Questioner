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

            meetup = self.check_item_exists(
                "id", meetup_id, self.meetups)

            if self.check_is_error(user):
                raise NotFound("User not found")

            if self.check_is_error(meetup):
                raise NotFound("This Meetup is not found")

            rsvp = {
                "id": len(self.rsvps) + 1,
                "meetup": meetup[0]["id"],
                "user": user[0]["id"],
                "response": details["response"]
            }

            self.rsvps.append(rsvp)

            resp = {
                "id": rsvp["id"],
                "meetup": rsvp["meetup"],
                "topic": meetup[0]["topic"],
                "status": rsvp["response"]
            }

            return self.makeresp(resp, 201)

        except KeyError as error:
            raise BadRequest("{} is a required data field".format(error))
