from flask import Flask, request, jsonify
from .. import version2
from .. models.question_model import QuestionModels


@version2.route("/questions", methods=["POST"])
def create_question():
    """ Creates a question for a specific meetup """

    header = request.headers.get("Authorization")

    if not header:
        return jsonify(
            {"error": "This resource is secured. Please provide authorization header",
             "status": 400}
        ), 400

    auth_token = header.split(" ")[1]

    response = QuestionModels().validate_token_status(auth_token)

    if isinstance(response, str):
        return jsonify(
            {"error": response,
             "status": 400}
        ), 400

    details = request.get_json()

    if not isinstance(details["user"], int):
        return jsonify({"error": "user must an integer", "status": 400}), 400

    if not isinstance(details["meetup"], int):
        return jsonify({"error": "Meetup must an integer", "status": 400}), 400

    resp = QuestionModels(details).create_question()

    return jsonify(resp), resp["status"]


