from datetime import datetime
from .common_model import CommonModels
from .user_model import users

# This array meetups, stores all meetup records created

meetups = []


class MeetupModels(CommonModels):
    """ 
    This class MeetupModels contain all the methods that
    interact with meetup details and records
    """

    def __init__(self):
        self.db = meetups

    def create_meetup(self, details):
        """ Creates a meetup record given data """

        images = []

        required = ["username", "tags", "location", "happeningOn", "topic"]

        missing = [key for key in required if not key in details.keys()]

        if missing:
            return self.makeresp("{} is missing in the data provided".format(missing[0]), 400)

        for key, value in details.items():
            if not value:
                return self.makeresp("{} is a cannot be empty".format(key), 400)
            if key == "images" and value:
                images = details["images"]

        payload = {
            "id": len(self.db) + 1,
            "createdOn": datetime.now(),
            "location": details["location"],
            "images": images,
            "topic": details["topic"],
            "happeningOn": datetime.strptime(details["happeningOn"], "%b %d %Y %I:%M%p"),
            "Tags": details["tags"],
            "createdBy": details["username"]
        }

        self.db.append(payload)

        resp = {
            "topic": payload["topic"],
            "location": payload["location"],
            "happeningOn": details["happeningOn"],
            "tags": payload["Tags"]
        }

        return self.makeresp(resp, 201)

    def fetch_specific_meetup(self, meetup_id):
        """ Fetches a specific meetup record  """
        meetup = [meetup for meetup in self.db if meetup["id"] == meetup_id]

        if not meetup:
            return self.makeresp("Meetup not found", 404)

        resp = {
            "id": meetup[0]["id"],
            "topic": meetup[0]["topic"],
            "location": meetup[0]["location"],
            "happeningOn": "{:%B %d, %Y %I:%M%p}".format(meetup[0]["happeningOn"]),
            "tags": meetup[0]["Tags"]
        }

        return self.makeresp(resp, 200)