from flask import Flask, request, jsonify
from .. import version2
from .. models.rsvp_model import RsvpModels


@version2.route("/meetups/<int:meetup_id>/rsvps", methods=["POST"])
def respond_meetup(meetup_id):
    """ Responds to meetup RSVP """

    details = request.get_json()

    checks = [RsvpModels().check_authorization(),
              RsvpModels().check_if_is_integer(details)]

    error_response = [response for response in checks if response]

    if error_response:
        return error_response[0]

    resp = RsvpModels(details).respond_meetup(meetup_id)

    return jsonify(resp), resp["status"]
