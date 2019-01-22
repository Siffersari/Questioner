from flask import Flask, request, jsonify, make_response
from .. import version2
from .. models.question_model import QuestionModels


@version2.route("/questions", methods=["POST"])
def create_question():
    """ Creates a question for a specific meetup """

    details = request.get_json()

    if QuestionModels().check_authorization():

        return QuestionModels().check_authorization()

    elif QuestionModels().check_if_is_integer(details):

        return QuestionModels().check_if_is_integer(details)

    resp = QuestionModels(details).create_question()

    return jsonify(resp), resp["status"]


@version2.route("/questions", methods=["GET"])
def fetch_all_questions():
    """ Returns all question records on the platform """

    if not QuestionModels().check_authorization():

        return jsonify(QuestionModels().fetch_all_questions()), 200

    return QuestionModels().check_authorization()


@version2.route("/questions/<int:question_id>/upvote", methods=["PATCH"])
def upvote_question(question_id):
    """ 
    This method upvotes a specific question 
    """
    details = request.get_json()

    if QuestionModels().check_authorization():

        return QuestionModels().check_authorization()

    if QuestionModels().check_if_is_integer(details):

        return QuestionModels().check_if_is_integer(details)

    return jsonify(QuestionModels(details).upvote_question(question_id)), 200


@version2.route("/questions/<int:question_id>/downvote", methods=["PATCH"])
def downvote_question(question_id):
    """ Downvotes a question to a specific meetup """

    if not request.headers.get("Authorization"):
        resp = {"error": "This resource is secured. Please provide authorization header",
                "status": 400}

        return jsonify(resp), resp["status"]

    auth_token = request.headers.get("Authorization").split(" ")[1]

    if isinstance(QuestionModels().validate_token_status(auth_token), str):
        return jsonify(
            {"error": QuestionModels().validate_token_status(auth_token),
             "status": 400}
        ), 400

    details = request.get_json()

    if QuestionModels().check_if_is_integer(details):

        return QuestionModels().check_if_is_integer(details)

    resp = jsonify(QuestionModels(details).downvote_question(question_id))

    status = QuestionModels(details).downvote_question(question_id)["status"]

    return resp, status


@version2.route("/comments", methods=["POST"])
def post_comment():
    """ Posts a comment to a question """

    details, not_authorized = request.get_json(), QuestionModels().check_authorization()

    if not_authorized:

        return QuestionModels().check_authorization()

    if QuestionModels().check_if_is_integer(details):

        respond = QuestionModels().check_if_is_integer(details)

        return respond

    resp = QuestionModels(details).post_comment()

    return make_response(jsonify(resp), resp["status"])


@version2.route("/questions/<int:question_id>", methods=["GET"])
def fetch_specific_question(question_id):
    """
    Fetches a question record given the question id 
    """

    check = QuestionModels().check_authorization()

    if not check:

        response = QuestionModels().fetch_specific_question(question_id)

        return jsonify(response), response["status"]

    else:
        return check
