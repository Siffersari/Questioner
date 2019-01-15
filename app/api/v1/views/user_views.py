from flask import Flask, request, jsonify
from .. import version1
from .. models.user_model import UserModels
from werkzeug.security import check_password_hash
from werkzeug.exceptions import BadRequest

db = UserModels()


@version1.route("/users", methods=["GET"])
def hello():
    """ List of all registered users """
    resp = db.fetch_users()

    return jsonify(resp)


@version1.route("/auth/signup", methods=["POST"])
def register_user():
    """ Registers a user given details """
    data = request.get_json()

    resp = db.register_user(data)

    return jsonify(resp), resp["status"]


@version1.route("/auth/login", methods=["POST"])
def login_user():
    """ Logs in a registered user """
    data = request.get_json()
    try:
        password = data["password"],
        username = data["username"]
    except KeyError as p:
        return jsonify({"error" : "{} should be present in the provided data".format(p), "status": 400}, 400)
            
    resp = db.login_user(data)

    return jsonify(resp), resp["status"]
