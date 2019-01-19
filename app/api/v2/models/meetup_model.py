from datetime import datetime
from .base_model import BaseModels
from ..utils.validators import DataValidators
from ..utils.sql_helpers import SqlHelper
from flask import current_app
from ....db_con import create_tables
from .user_model import UserModels


class MeetupModels(BaseModels):
    """
    This class MeetupModels contain all the methods that
    interact with meetup details and records
    """

    def __init__(self, details={}):
        self.meetup_details = details
        self.db = create_tables()
        self.sql = SqlHelper()

    def create_meetup(self):
        """ Creates a meetup record given data """
        images = []

        try:
            images = self.meetup_details["images"]
        except:
            pass

        try:
            isempty = DataValidators(
                self.meetup_details).check_values_not_empty()

            if isinstance(isempty, str):
                return self.makeresp(isempty, 400)

            user = self.sql.get_username_by_id(
                int(self.meetup_details["user"]))

            if not user:
                return self.makeresp("This user is not found", 404)

            payload = {
                "createdOn": datetime.now(),
                "location": self.meetup_details["location"],
                "images": images,
                "topic": self.meetup_details["topic"],
                "happeningOn": self.meetup_details["happeningOn"],
                "Tags": self.meetup_details["tags"],
                "createdBy": self.meetup_details["user"]
            }

            is_admin = self.sql.get_admin_user(self.meetup_details["user"])

            if self.check_is_error(is_admin):
                status = 403
                if 'Administrator' in is_admin:
                    status = 404

                return self.makeresp(is_admin, status)

            # Add meetup details to the database

            meetup_id = SqlHelper(payload).save_meetup()

            resp = {
                "topic": payload["topic"],
                "location": payload["location"],
                "happeningOn": self.meetup_details["happeningOn"],
                "id": meetup_id,
                "images": images,
                "tags": payload["Tags"],
                "createdOn": payload["createdOn"],
                "createdBy": user[0]
            }

            return self.makeresp(resp, 201)

        except KeyError as missing:
            return self.makeresp("{} can not be empty".format(missing), 400)

    def fetch_specific_meetup(self, meetup_id):
        """ Fetches a specific meetup record  """
        meetup = self.sql.fetch_details_by_id(
            "meetup_id", meetup_id, "meetups")

        if not meetup:
            return self.makeresp("Meetup not found", 404)

        username = self.sql.get_username_by_id(meetup[1])

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

        meetups = self.sql.get_upcoming_meetups()

        resp = []

        for items in meetups:
            meetup_id, user_id, topic, happening_on, location, images, tags, created_on = items

            user = self.sql.get_username_by_id(user_id)

            meetup = {
                "id": meetup_id,
                "topic": topic,
                "location": location,
                "happeningOn": happening_on,
                "tags": tags,
                "createdBy": user,
                "createdOn": created_on
            }
            resp.append(meetup)

        return self.makeresp(resp, 200)

    def delete_meetup(self, meetup_id):
        """ Accepts a meetup_id and deletes meetup record """
        meetup = self.sql.fetch_details_by_id(
            "meetup_id", meetup_id, "meetups")

        if not meetup:
            return self.makeresp("Meetup not found", 404)

        user = self.sql.get_username_by_id(
            int(self.meetup_details["user"]))

        if not user:
            return self.makeresp("This user is not found", 404)

        is_admin = self.sql.get_admin_user(self.meetup_details["user"])

        if self.check_is_error(is_admin):
            status = 403
            if 'Administrator' in is_admin:
                status = 404

            return self.makeresp(is_admin, status)

        self.sql.delete_meetup(meetup_id)

        return self.makeresp(["This meetup has been deleted successfully"], 200)

    def post_images(self, meetup_id):
        """ Adds images to a meetup record """

        try:
            images = self.meetup_details["images"]

        except KeyError as key:
            return self.makeresp("{} is a required field".format(key), 400)

        isempty = DataValidators(
            self.meetup_details).check_values_not_empty()

        if isinstance(isempty, str):
            return self.makeresp(isempty, 400)

        meetup = self.sql.fetch_details_by_id(
            "meetup_id", meetup_id, "meetups")

        if not meetup:
            return self.makeresp("Meetup not found", 404)

        user = self.sql.get_username_by_id(
            int(self.meetup_details["user"]))

        if not user:
            return self.makeresp("This user is not found", 404)

        is_admin = self.sql.get_admin_user(self.meetup_details["user"])

        if self.check_is_error(is_admin):
            status = 403
            if 'Administrator' in is_admin:
                status = 404

            return self.makeresp(is_admin, status)

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

        isempty = DataValidators(
            self.meetup_details).check_values_not_empty()

        if isinstance(isempty, str):
            return self.makeresp(isempty, 400)

        meetup = self.sql.fetch_details_by_id(
            "meetup_id", meetup_id, "meetups")

        if not meetup:
            return self.makeresp("Meetup not found", 404)

        user = self.sql.get_username_by_id(
            int(self.meetup_details["user"]))

        if not user:
            return self.makeresp("This user is not found", 404)

        is_admin = self.sql.get_admin_user(self.meetup_details["user"])

        if self.check_is_error(is_admin):
            status = 403
            if 'Administrator' in is_admin:
                status = 404

            return self.makeresp(is_admin, status)

        tags = SqlHelper(self.meetup_details).get_tags(meetup_id)

        if self.check_is_error(tags):
            updtags = SqlHelper(self.meetup_details).add_tags(meetup_id)

            return self.makeresp({
                "meetup": meetup[0],
                "topic": meetup[2],
                "tags": updtags
            }, 201)

        self.meetup_details["tags"] = tags + \
            [tag for tag in tags_data if not tag in tags]

        tags = SqlHelper(self.meetup_details).add_tags(meetup_id)

        response = {
            "meetup": meetup[0],
            "topic": meetup[2],
            "tags": self.meetup_details["tags"]
        }

        return self.makeresp(response, 201)
