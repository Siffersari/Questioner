from flask import Flask, request, jsonify
from .. import version2
from .. models.meetup_model import MeetupModels


@version2.route("/meetups", methods=["POST"])
def post_new_meetup():
    """ Creates a new meetup record if details provided"""

    header = request.headers.get("Authorization")

    if not header:
        return jsonify(
            {"error": "This resource is secured. Please provide authorization header",
             "status": 400}
        ), 400

    auth_token = header.split(" ")[1]

    response = MeetupModels().validate_token_status(auth_token)

    if isinstance(response, str):
        return jsonify(
            {"error": response,
             "status": 400}
        ), 400
    data = request.get_json()

    try:
        if not isinstance(data["user"], int):
            return jsonify({"error": "user must an integer", "status": 400}), 400

    except KeyError as keyerr:
        return jsonify({"error": "{} is  a required key".format(keyerr), "status": 400}), 400

    resp = MeetupModels(data).create_meetup()

    return jsonify(resp), resp["status"]


@version2.route("/meetups/<int:meetup_id>", methods=["GET"])
def fetch_specific_meetup(meetup_id):
    """ Fetches a specific meetup record given meetup_id """

    header = request.headers.get("Authorization")

    if not header:
        return jsonify(
            {"error": "This resource is secured. Please provide authorization header",
             "status": 400}
        ), 400

    auth_token = header.split(" ")[1]

    response = MeetupModels().validate_token_status(auth_token)

    if isinstance(response, str):
        return jsonify(
            {"error": response,
             "status": 400}
        ), 400

    return jsonify(MeetupModels().fetch_specific_meetup(meetup_id)), MeetupModels().fetch_specific_meetup(meetup_id)["status"]


@version2.route("/meetups/upcoming", methods=["GET"])
def fetch_upcoming_meetup():
    """ Fetches all upcoming meetup records """

    header = request.headers.get("Authorization")

    if not header:
        return jsonify(
            {"error": "This resource is secured. Please provide authorization header",
             "status": 400}
        ), 400

    auth_token = header.split(" ")[1]

    response = MeetupModels().validate_token_status(auth_token)

    if isinstance(response, str):
        return jsonify(
            {"error": response,
             "status": 400}
        ), 400

    return jsonify(MeetupModels().fetch_upcoming_meetups()), MeetupModels().fetch_upcoming_meetups()["status"]
