from .common_model import CommonModels


# This array, rsvps, stores all rsvps to meetups on the platfrom


class RsvpModels(CommonModels):
    """
    This class RsvpModels contains all the methods that
    are used to manipulated rsvps of a specific meetup
    """

    def respond_meetup(self, details, meetup_id):
        """ Responds to a meetup RSVP """

        if self.check_is_error(self.check_missing_details(details)):
            return self.makeresp(self.check_missing_details(details), 400)

        try:

            user = self.check_item_exists(
                "id", int(details["user"]), self.users)

            meetup = self.check_item_exists(
                "id", meetup_id, self.meetups)

            if self.check_is_error(user):
                return self.makeresp("User not found", 404)

            if self.check_is_error(meetup):
                return self.makeresp("This Meetup is not found", 404)

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

        except Exception as error:
            return self.makeresp("{} is a required data field".format(error), 400)
