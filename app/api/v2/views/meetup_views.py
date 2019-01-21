from flask import Flask, request, jsonify
from .. import version2
from .. models.meetup_model import MeetupModels


@version2.route("/meetups", methods=["POST"])
def post_new_meetup():
    """ Creates a new meetup record if details provided"""

    if MeetupModels().check_authorization():

        return MeetupModels().check_authorization()

    elif MeetupModels().check_if_is_integer(request.get_json()):

        return MeetupModels().check_if_is_integer(request.get_json())

    resp = MeetupModels(request.get_json()).create_meetup()

    return jsonify(resp), resp["status"]


@version2.route("/meetups/<int:meetup_id>", methods=["GET"])
def fetch_specific_meetup(meetup_id):
    """ Fetches a specific meetup record given meetup_id """

    if MeetupModels().check_authorization():

        return MeetupModels().check_authorization()

    return jsonify(MeetupModels().fetch_specific_meetup(meetup_id)), MeetupModels().fetch_specific_meetup(meetup_id)["status"]


@version2.route("/meetups/upcoming", methods=["GET"])
def fetch_upcoming_meetup():
    """ Fetches all upcoming meetup records """

    if MeetupModels().check_authorization():

        return MeetupModels().check_authorization()

    response = MeetupModels().fetch_upcoming_meetups()

    status = response["status"]

    return jsonify(response), status


@version2.route("/meetups/<int:meetup_id>", methods=['DELETE'])
def delete_meetup(meetup_id):
    """ Deletes a meetup record """

    if MeetupModels().check_authorization():

        return MeetupModels().check_authorization()

    details = request.get_json()

    if MeetupModels().check_if_is_integer(details):

        return MeetupModels().check_if_is_integer(details)

    response = MeetupModels(details).delete_meetup(meetup_id)

    return jsonify(response), response["status"]


@version2.route("/meetups/<int:meetup_id>/images", methods=["POST"])
def post_images(meetup_id):
    """ Add images to a meetup """

    if MeetupModels().check_authorization():

        return MeetupModels().check_authorization()

    details = request.get_json()

    if MeetupModels().check_if_is_integer(details):

        return MeetupModels().check_if_is_integer(details)

    status = MeetupModels(details).post_images(meetup_id)["status"]

    return jsonify(MeetupModels(details).post_images(meetup_id)), status


@version2.route("/meetups/<int:meetup_id>/tags", methods=["POST"])
def add_tags(meetup_id):
    """ Add tags to a meetup """

    if MeetupModels().check_authorization():

        return MeetupModels().check_authorization()

    details = request.get_json()

    if MeetupModels().check_if_is_integer(details):

        return MeetupModels().check_if_is_integer(details)

    response = MeetupModels(details).add_tags(meetup_id)

    return jsonify(response), MeetupModels(details).add_tags(meetup_id)["status"]
