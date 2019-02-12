from flask import Flask, request, jsonify
from .. import version2
from .. models.user_model import UserModels
from werkzeug.security import check_password_hash


@version2.route("/users", methods=["GET"])
def fetch_user():
    """ List of all registered users """

    if not isinstance(UserModels().check_authorization(), int):

        return UserModels().check_authorization()

    else:

        user_id = UserModels().check_authorization()

    resp = UserModels().fetch_user(user_id)

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


@version2.route("/auth/logout", methods=["POST"])
def logout_user():
    """ Log out user """

    decoded_auth = UserModels().check_authorization()

    if not isinstance(decoded_auth, int):

        return decoded_auth

    auth_token = request.headers.get("Authorization").split(" ")[1]

    response = UserModels().logout_user(auth_token)

    return jsonify(response), response["status"]


@version2.route("/users/<string:email>", methods=["GET"])
def request_password_reset(email):
    """ Requests for a password reset """

    response = UserModels().request_password_reset(email)

    return jsonify(response), response["status"]


@version2.route("/auth/reset_password/<token>")
def reset_password(token):
    """ Resets password """

    decoded_auth = UserModels().check_authorization()

    if isinstance(decoded_auth, int):

        return jsonify(UserModels().makeresp("This token is invalid", 400))

    if not "@" in decoded_auth:

        return decoded_auth

    details = request.get_json()

    try:
        details["email"] = decoded_auth

    except:
        
        return jsonify(UserModels().makeresp("Please provide data as JSON format", 400))

    response = UserModels(details).reset_password()

    return jsonify(response), response["status"]
