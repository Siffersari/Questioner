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
