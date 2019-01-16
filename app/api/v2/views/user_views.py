from flask import Flask, request, jsonify
from .. import version2
from .. models.user_model import UserModels
from werkzeug.security import check_password_hash


@version2.route("/users", methods=["GET"])
def fetch_all_users():
    """ List of all registered users """
    resp = UserModels().fetch_users()

    return jsonify(resp)


@version2.route("/auth/signup", methods=["POST"])
def register_user():
    """ Registers a user given details """
    data = request.get_json()

    resp = UserModels(data).register_user()

    return jsonify(resp), resp["status"]


@version2.route("/auth/login", methods=["POST"])
def login_user():
    """ Logs in a registered user """
    data = request.get_json()
    try:
        password = data["password"],
        username = data["username"]
    except KeyError as p:
        return jsonify({"error": "{} should be present in the provided data".format(p), "status": 400}), 400

    resp = UserModels(data).login_user()

    return jsonify(resp), resp["status"] 
