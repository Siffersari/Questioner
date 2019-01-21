from .base_model import BaseModels
from ..utils.validators import DataValidators
from ..utils.sql_helpers import SqlHelper
from flask import current_app
from ....db_con import create_tables


class RsvpModels(BaseModels):
    """
    This class RsvpModels contains all the methods that
    are used to manipulated rsvps of a specific meetup
    """

    def __init__(self, details={}):
        self.db = create_tables()
        self.rsvp_details = details
        self.sql = SqlHelper()

    def respond_meetup(self, meetup_id):
        """ Responds to a meetup RSVP """

        locations = ["user_id", "meetup_id", "response"]

        isempty = DataValidators(
            self.rsvp_details).check_values_not_empty()

        if isinstance(isempty, str):
            return self.makeresp(isempty, 400)

        try:
            user = self.sql.get_username_by_id(
                int(self.rsvp_details["user"]))

            response = self.rsvp_details["response"]
        except KeyError as error:
            return self.makeresp("{} is a required data key".format(error), 400)

        meetup = self.sql.fetch_details_by_id(
            "meetup_id", meetup_id, "meetups")

        if not user:
            return self.makeresp("User not found", 404)

        if not meetup:
            return self.makeresp("Meetup not found", 404)

        validresp = ["yes", "Yes", "YES", "no", "No", "NO", "maybe", "Maybe"]

        if response not in validresp:
            return self.makeresp("Your answer may only take one of the form {}".format(validresp), 400)

        rsvp = {
            "user": self.rsvp_details["user"],
            "meetup": meetup_id,
            "response": response
        }

        rsvp_id = SqlHelper(rsvp).save_to_database(locations, "rsvps")

        resp = {
            "id": rsvp_id,
            "meetup": rsvp["meetup"],
            "topic": meetup[2],
            "status": rsvp["response"]
        }

        return self.makeresp(resp, 201)
