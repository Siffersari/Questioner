from flask import Flask, request, jsonify
from .. import version1
from .. models.question_model import QuestionModels

db = QuestionModels()


@version1.route("/questions", methods=["POST"])
def create_question():
    """ Creates a question for a specific meetup """

    details = request.get_json()

    resp = db.create_question(details)

    return jsonify(resp), resp["status"]


@version1.route("/questions/<int:question_id>/upvote", methods=["PATCH"])
def upvote_question(question_id):
    """ 
    This method upvotes a specific question 
    """
    return jsonify(db.upvote_question(question_id)), 200


@version1.route("/questions/<int:question_id>/downvote", methods=["PATCH"])
def downvote_question(question_id):
    """ Downvotes a question to a specific meetup """

    resp = db.downvote_question(question_id)

    return jsonify(resp), resp["status"]
