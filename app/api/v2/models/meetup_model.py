from datetime import datetime
from .base_model import BaseModels
from ..utils.validators import DataValidators
from ..utils.sql_helpers import SqlHelper
from flask import current_app
from ....db_con import create_tables
from .user_model import UserModels


def validate_meetup(details):
    """ Checks whether user and meetup exists """

    try:
        isempty = DataValidators(
            details).check_values_not_empty()

        if isinstance(isempty, str):
            return MeetupModels().makeresp(isempty, 400)

        if not SqlHelper().get_username_by_id(
                int(details["user"])):

            return MeetupModels().makeresp("This user is not found", 404)

        is_admin = SqlHelper().get_admin_user(details["user"])

        if MeetupModels().check_is_error(is_admin):
            status = 403
            if 'Administrator' in is_admin:
                status = 404

            return UserModels().makeresp(is_admin, status)

        return SqlHelper().get_username_by_id(
            int(details["user"]))

    except KeyError as missing:

        return UserModels().makeresp("Expected {} key to be present in the data but found none".format(missing), 400)


def check_meetup_exists(meetup_id):

    meetup = SqlHelper().fetch_details_by_id(
        "meetup_id", meetup_id, "meetups")

    if not meetup:
        return MeetupModels().makeresp("Meetup not found", 404)

    return meetup


class MeetupModels(BaseModels):
    """
    This class MeetupModels contain all the methods that
    interact with meetup details and records
    """

    def __init__(self, details={}):

        self.meetup_details = details

    def create_meetup(self):
        """ Creates a meetup record given data """

        images, locations = [], ["user_id", "topic",
                                 "location", "happening_on", "images", "tags"]
        try:
            images = self.meetup_details["images"]
        except:
            pass

        try:
            topic, tags, happeningOn, location = self.meetup_details["topic"], self.meetup_details[
                "tags"], self.meetup_details["happeningOn"], self.meetup_details["location"]

        except KeyError as errkey:
            return UserModels().makeresp("Expected {} key to be present in the data but found none".format(errkey), 400)

        user = validate_meetup(self.meetup_details)

        if not isinstance(user, tuple):

            return user

        payload = {
            "createdBy": self.meetup_details["user"],
            "topic": topic,
            "location": location,
            "happeningOn": happeningOn,
            "images": images,
            "Tags": tags,
        }

        meetup_id = SqlHelper(payload).save_to_database(
            locations, "meetups")

        resp = {
            "topic": payload["topic"],
            "location": payload["location"],
            "happeningOn": self.meetup_details["happeningOn"],
            "id": meetup_id,
            "images": images,
            "tags": payload["Tags"],
            "createdOn": datetime.now(),
            "createdBy": user[0]

        }

        return self.makeresp(resp, 201)

    def fetch_specific_meetup(self, meetup_id):
        """ Fetches a specific meetup record  """

        meetup = check_meetup_exists(meetup_id)

        if not isinstance(meetup, tuple):

            return meetup

        username = SqlHelper().get_username_by_id(meetup[1])

        resp = {
            "id": meetup_id,
            "topic": meetup[2],
            "location": meetup[4],
            "happeningOn": "{:%B %d, %Y %I:%M%p}".format(meetup[3]),
            "tags": meetup[6],
            "images": meetup[5],
            "createdOn": meetup[7],
            "createdBy": username[0]
        }

        return self.makeresp(resp, 200)

    def fetch_upcoming_meetups(self):
        """ Fetches all upcoming meetups """

        meetups = SqlHelper().get_upcoming_meetups()

        resp = []

        for items in meetups:

            user = SqlHelper().get_username_by_id(items[1])[0]

            meetup = {
                "id": items[0],
                "topic": items[2],
                "location": items[4],
                "happeningOn": items[3],
                "tags": items[6],
                "createdBy": user,
                "createdOn": items[7]
            }
            resp.append(meetup)

        return self.makeresp(resp, 200)

    def delete_meetup(self, meetup_id):
        """ Accepts a meetup_id and deletes meetup record """

        meetup = check_meetup_exists(meetup_id)

        if not isinstance(meetup, tuple):

            return meetup

        user = validate_meetup(self.meetup_details)

        if not isinstance(user, tuple):

            return user
        SqlHelper().delete_meetup(meetup_id)

        return self.makeresp(["This meetup has been deleted successfully"], 200)

    def post_images(self, meetup_id):
        """ Adds images to a meetup record """

        meetup = check_meetup_exists(meetup_id)

        if not isinstance(meetup, tuple):

            return meetup

        user = validate_meetup(self.meetup_details)

        if not isinstance(user, tuple):

            return user

        updated_img = SqlHelper(self.meetup_details).get_images(meetup_id)

        if self.check_is_error(updated_img):
            updimages = SqlHelper(self.meetup_details).post_images(meetup_id)

            return self.makeresp({
                "meetup": meetup[0],
                "topic": meetup[2],
                "images": updimages
            }, 201)

        self.meetup_details["images"] = updated_img + \
            self.meetup_details["images"]

        updated_img = SqlHelper(self.meetup_details).post_images(meetup_id)

        response = {
            "meetup": meetup[0],
            "topic": meetup[2],
            "images": self.meetup_details["images"]
        }

        return self.makeresp(response, 201)

    def add_tags(self, meetup_id):
        """ Adds images to a meetup record """

        try:
            tags_data = self.meetup_details["tags"]

        except KeyError as key:
            return self.makeresp("{} is a required field".format(key), 400)

        user = validate_meetup(self.meetup_details)

        if not isinstance(user, tuple):

            return user

        meetup = check_meetup_exists(meetup_id)

        if not isinstance(meetup, tuple):

            return meetup

        tags = SqlHelper(self.meetup_details).get_tags(meetup_id)

        if isinstance(tags, str):

            return self.makeresp({
                "meetup": meetup[0],
                "topic": meetup[2],
                "tags": SqlHelper(self.meetup_details).add_tags(meetup_id)
            }, 201)

        self.meetup_details["tags"] = tags + \
            [tag for tag in tags_data if not tag in tags]

        tags = SqlHelper(self.meetup_details).add_tags(meetup_id)

        return self.makeresp({
            "meetup": meetup[0],
            "topic": meetup[2],
            "tags": self.meetup_details["tags"]
        }, 201)
