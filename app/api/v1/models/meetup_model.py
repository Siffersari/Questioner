from datetime import datetime
from .common_model import CommonModels


class MeetupModels(CommonModels):
    """ 
    This class MeetupModels contain all the methods that
    interact with meetup details and records
    """

    def create_meetup(self, details):
        """ Creates a meetup record given data """
        images = []

        try:
            images = details["images"]
        except:
            pass

        try:
            payload = {
                "id": len(self.meetups) + 1,
                "createdOn": datetime.now(),
                "location": details["location"],
                "images": images,
                "topic": details["topic"],
                "happeningOn": datetime.strptime(details["happeningOn"], "%b %d %Y %I:%M%p"),
                "Tags": details["tags"],
                "createdBy": details["username"]
            }

            self.meetups.append(payload)

            resp = {
                "topic": payload["topic"],
                "location": payload["location"],
                "happeningOn": details["happeningOn"],
                "id": payload["id"],
                "tags": payload["Tags"]
            }

            return self.makeresp(resp, 201)

        except KeyError as missing:
            return self.makeresp("{} can not be empty".format(missing), 400)

    def fetch_specific_meetup(self, meetup_id):
        """ Fetches a specific meetup record  """
        meetup = self.check_item_exists("id", meetup_id, self.meetups)

        if self.check_is_error(meetup):
            return self.makeresp("Meetup not found", 404)

        resp = {
            "id": meetup[0]["id"],
            "topic": meetup[0]["topic"],
            "location": meetup[0]["location"],
            "happeningOn": "{:%B %d, %Y %I:%M%p}".format(meetup[0]["happeningOn"]),
            "tags": meetup[0]["Tags"]
        }

        return self.makeresp(resp, 200)

    def fetch_upcoming_meetups(self):
        """ Fetches all upcoming meetups """
        resp = self.meetups

        return self.makeresp(resp, 200)
