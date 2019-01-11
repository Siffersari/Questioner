from flask import Flask, request, jsonify
from .. import version1
from .. models.meetup_model import MeetupModels

db = MeetupModels()

@version1.route("/meetups", methods=["POST"])
def post_new_meetup():
    """ Creates a new meetup record if details provided"""

    resp = db.create_meetup(request.get_json())

    return jsonify(resp), resp["status"]

@version1.route("/meetups/<int:meetup_id>", methods=["GET"])
def fetch_specific_meetup(meetup_id):
    """ Fetches a specific meetup record """
    
    if db.fetch_specific_meetup(meetup_id):
        return jsonify(db.fetch_specific_meetup(meetup_id)), db.fetch_specific_meetup(meetup_id)["status"]


@version1.route("/meetups/upcoming", methods=["GET"])
def fetch_upcoming_meetup():
    """ Fetches all upcoming meetup records """
   
    return jsonify(db.fetch_upcoming_meetups()), db.fetch_upcoming_meetups()["status"]