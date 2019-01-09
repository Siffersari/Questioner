from flask import Flask, request, jsonify
from .. import version1
from .. models.meetup_model import MeetupModels

db = MeetupModels()

@version1.route("/meetups", methods=["POST"])
def create_meetup():
    """ Creates a meetup record if data """
    meetup = request.get_json()

    resp = db.create_meetup(meetup)

    return jsonify(resp), resp["status"]

@version1.route("/meetups/<int:meetup_id>", methods=["GET"])
def fetch_specific_meetup(meetup_id):
    """ Fetches a specific meetup record """
    
    resp = db.fetch_specific_meetup(meetup_id)

    return jsonify(resp), resp["status"]


@version1.route("/meetups/upcoming", methods=["GET"])
def fetch_upcoming_meetup():
    """ Fetches all upcoming meetup records """

    resp = db.fetch_upcoming_meetups()
    
    return jsonify(resp), resp["status"]