from flask import Flask, request, jsonify
from .. import version2
from .. models.meetup_model import MeetupModels


@version2.route("/meetups", methods=["POST"])
def post_new_meetup():
    """ Creates a new meetup record if details provided"""

    decoded_auth = MeetupModels().check_authorization()

    if not isinstance(decoded_auth, int):

        return decoded_auth

    data = request.get_json()

    data["user"] = decoded_auth

    resp = MeetupModels(data).create_meetup()

    return jsonify(resp), resp["status"]


@version2.route("/meetups/<int:meetup_id>", methods=["GET"])
def fetch_specific_meetup(meetup_id):
    """ Fetches a specific meetup record given meetup_id """

    decoded_auth = MeetupModels().check_authorization()

    if not isinstance(decoded_auth, int):

        return decoded_auth

    response = MeetupModels().fetch_specific_meetup(meetup_id)

    return jsonify(response), response["status"]


@version2.route("/meetups/upcoming", methods=["GET"])
def fetch_upcoming_meetup():
    """ Fetches all upcoming meetup records """

    response = MeetupModels().fetch_upcoming_meetups()

    status = response["status"]

    return jsonify(response), status


@version2.route("/meetups/<int:meetup_id>", methods=['DELETE'])
def delete_meetup(meetup_id):
    """ Deletes a meetup record """

    decoded_auth = MeetupModels().check_authorization()

    if not isinstance(decoded_auth, int):

        return decoded_auth

    details = {
        "user": decoded_auth
    }

    response = MeetupModels(details).delete_meetup(meetup_id)

    return jsonify(response), response["status"]


@version2.route("/meetups/<int:meetup_id>/images", methods=["POST"])
def post_images(meetup_id):
    """ Add images to a meetup """

    decoded_auth = MeetupModels().check_authorization()

    if not isinstance(decoded_auth, int):

        return decoded_auth

    details = request.get_json()

    details["user"] = decoded_auth

    try:

        images = details["images"]

    except KeyError as missingkey:

        return MeetupModels().makeresp("Expected {} key to be present in the provided data but found none ".format(missingkey), 400)

    status = MeetupModels(details).post_images(meetup_id)["status"]

    return jsonify(MeetupModels(details).post_images(meetup_id)), status


@version2.route("/meetups/<int:meetup_id>/tags", methods=["POST"])
def add_tags(meetup_id):
    """ Add tags to a meetup """

    decoded_auth = MeetupModels().check_authorization()

    if not isinstance(decoded_auth, int):

        return decoded_auth

    details = request.get_json()

    details["user"] = decoded_auth

    response = MeetupModels(details).add_tags(meetup_id)

    return jsonify(response), MeetupModels(details).add_tags(meetup_id)["status"]


@version2.route("/meetups/<string:topic>/<string:location>", methods=["GET"])
def fetch_meetup_id(topic, location):
    """ Fetches a meetup id given location and topic """

    decoded_auth = MeetupModels().check_authorization()

    if not isinstance(decoded_auth, int):

        return decoded_auth

    details = {
        "topic": topic,
        "location": location,
        "user": decoded_auth
    }

    response = MeetupModels(details).fetch_meetup_id_by_details()

    return jsonify(response), response["status"]


@version2.route("/meetups/<int:meetup_id>/questions", methods=["GET"])
def fetch_meetup_questions(meetup_id):
    """ Fetches all questions to a meetup record """

    check = MeetupModels().check_authorization()

    if isinstance(check, int):

        return jsonify(MeetupModels().fetch_meetup_questions(meetup_id)), 200

    return check
