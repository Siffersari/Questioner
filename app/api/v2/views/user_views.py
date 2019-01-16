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
