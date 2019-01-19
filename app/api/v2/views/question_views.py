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


@version2.route("/questions/<int:question_id>/upvote", methods=["PATCH"])
def upvote_question(question_id):
    """ 
    This method upvotes a specific question 
    """
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

    try:
        if not isinstance(details["user"], int):
            return jsonify({"error": "user must be represented by an integer id", "status": 400}), 400

    except KeyError as keyerr:
        return jsonify({"error": "{} is  a required key".format(keyerr), "status": 400}), 400

    return jsonify(QuestionModels(details).upvote_question(question_id)), 200


@version2.route("/questions/<int:question_id>/downvote", methods=["PATCH"])
def downvote_question(question_id):
    """ Downvotes a question to a specific meetup """

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

    try:
        if not isinstance(details["user"], int):
            return jsonify({"error": "user must be represented by an integer id", "status": 400}), 400

    except KeyError as keyerr:
        return jsonify({"error": "{} is  a required key".format(keyerr), "status": 400}), 400

    resp = QuestionModels(details).downvote_question(question_id)

    return jsonify(resp), resp["status"]


@version2.route("/comments", methods=["POST"])
def post_comment():
    """ Posts a comment to a question """

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

    try:
        if not isinstance(details["user"], int):
            return jsonify({"error": "user must be represented by an integer id", "status": 400}), 400

    except KeyError as keyerr:
        return jsonify({"error": "{} is  a required key".format(keyerr), "status": 400}), 400

    resp = QuestionModels(details).post_comment()

    return jsonify(resp), resp["status"]
