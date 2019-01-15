from flask import Flask, request, jsonify
from .. import version1
from .. models.meetup_model import MeetupModels

db = MeetupModels()

@version1.route("/meetups", methods=["POST"])
def post_new_meetup():
    """ Creates a new meetup record if details provided"""

    data = request.get_json()

    try:
        if not isinstance(data["user"], int):
            return jsonify({"error": "user must an integer", "status": 400}), 400

    except KeyError as keyerr:
        return jsonify({"error": "{} is  a required key".format(keyerr), "status": 400}), 400

    resp = db.create_meetup(data)

    return jsonify(resp), resp["status"]

@version1.route("/meetups/<int:meetup_id>", methods=["GET"])
def fetch_specific_meetup(meetup_id):
    """ Fetches a specific meetup record """
        
    return jsonify(db.fetch_specific_meetup(meetup_id)), db.fetch_specific_meetup(meetup_id)["status"]


@version1.route("/meetups/upcoming", methods=["GET"])
def fetch_upcoming_meetup():
    """ Fetches all upcoming meetup records """
   
    return jsonify(db.fetch_upcoming_meetups()), db.fetch_upcoming_meetups()["status"]