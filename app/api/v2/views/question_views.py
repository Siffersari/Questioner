from flask import Flask, request, jsonify, make_response
from .. import version2
from .. models.question_model import QuestionModels


@version2.route("/questions", methods=["POST"])
def create_question():
    """ Creates a question for a specific meetup """

    details = request.get_json()

    decoded_auth = QuestionModels().check_authorization()

    if not isinstance(decoded_auth, int):

        return decoded_auth

    details["user"] = decoded_auth

    resp = QuestionModels(details).create_question()

    return jsonify(resp), resp["status"]


@version2.route("/questions", methods=["GET"])
def fetch_all_questions():
    """ Returns all question records on the platform """

    if isinstance(QuestionModels().check_authorization(), int):

        return jsonify(QuestionModels().fetch_all_questions()), 200

    return QuestionModels().check_authorization()


@version2.route("/questions/<int:question_id>/upvote", methods=["PATCH"])
def upvote_question(question_id):
    """ 
    This method upvotes a specific question 
    """

    decoded_auth = QuestionModels().check_authorization()

    if not isinstance(decoded_auth, int):

        return decoded_auth

    details = {
        "user": decoded_auth
    }

    response = QuestionModels(details).upvote_question(question_id)

    return jsonify(response), response["status"]


@version2.route("/questions/<int:question_id>/downvote", methods=["PATCH"])
def downvote_question(question_id):
    """ Downvotes a question to a specific meetup """

    if not request.headers.get("Authorization"):
        resp = {"error": "This resource is secured. Please provide authorization header",
                "status": 400}

        return jsonify(resp), resp["status"]

    auth_token = request.headers.get("Authorization").split(" ")[1]

    validation_response = QuestionModels().validate_token_status(auth_token)

    if not isinstance(validation_response, int):
        return jsonify(
            {"error": validation_response,
             "status": 400}
        ), 400

    details = {
        "user": validation_response
    }

    resp = QuestionModels(details).downvote_question(question_id)

    status = resp["status"]

    return jsonify(resp), status


@version2.route("/questions/<int:question_id>", methods=["GET"])
def fetch_specific_question(question_id):
    """
    Fetches a question record given the question id 
    """

    check = QuestionModels().check_authorization()

    if isinstance(check, int):

        response = QuestionModels().fetch_specific_question(question_id)

        return jsonify(response), response["status"]

    else:
        return check


@version2.route("/questions/<int:question_id>", methods=['DELETE'])
def delete_question(question_id):
    """ Deletes a question to a meetup record """

    if not isinstance(QuestionModels().check_authorization(), int):

        return QuestionModels().check_authorization()

    decoded_auth = QuestionModels().check_authorization()

    if not isinstance(decoded_auth, int):

        return decoded_auth

    details = {
        "user": decoded_auth
    }

    response = QuestionModels(details).delete_question(question_id)

    return jsonify(response), response["status"]
