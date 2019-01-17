from flask import Flask, request, jsonify
from .. import version2
from .. models.rsvp_model import RsvpModels


@version2.route("/meetups/<int:meetup_id>/rsvps", methods=["POST"])
def respond_meetup(meetup_id):
    """ Responds to meetup RSVP """

    header = request.headers.get("Authorization")

    if not header:
        return jsonify(
            {"error": "This resource is secured. Please provide authorization header",
             "status": 400}
        ), 400

    auth_token = header.split(" ")[1]

    response = RsvpModels().validate_token_status(auth_token)

    if isinstance(response, str):
        return jsonify(
            {"error": response,
             "status": 400}
        ), 400

    details = request.get_json()

    try:
        if not isinstance(details["user"], int):
            return jsonify({"error": "user must an integer", "status": 400}), 400

    except KeyError as keyerr:
        return jsonify({"error": "{} is  a required key".format(keyerr), "status": 400}), 400

    resp = RsvpModels(details).respond_meetup(meetup_id)

    return jsonify(resp), resp["status"]
