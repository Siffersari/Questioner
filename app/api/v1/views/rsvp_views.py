from flask import Flask, request, jsonify
from .. import version1
from .. models.rsvp_model import RsvpModels

db = RsvpModels()


@version1.route("/meetups/<int:meetup_id>/rsvps", methods=["POST"])
def respond_meetup(meetup_id):
    """ Responds to meetup RSVP """

    details = request.get_json()

    resp = db.respond_meetup(details, meetup_id)

    return jsonify(resp), resp["status"]
