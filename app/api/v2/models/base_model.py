import os
from flask import current_app, jsonify, request
from datetime import datetime, timedelta
from ..utils.sql_helpers import SqlHelper
import jwt


class BaseModels(object):
    """ 
    This class contains methods that are common to all other
    models
    """

    def makeresp(self, payload, status_code):
        """ Returns user details if found and message if not """

        if isinstance(payload, str):
            return {
                "status": status_code,
                "error": payload
            }
        if not isinstance(payload, list):
            return {
                "status": status_code,
                "data": [payload]
            }

        return {
            "status": status_code,
            "data": payload
        }

    def check_is_error(self, data):
        """ Checks if data passed to it is of type string """

        return isinstance(data, str)

    @staticmethod
    def give_auth_token(user_id):
        """ Generates a JWT auth token """
        app = os.getenv("SECRET_KEY")

        token_data = {
            "exp": datetime.utcnow() + timedelta(days=1),
            "iat": datetime.utcnow(),
            "sub": user_id
        }

        token = jwt.encode(
            token_data,
            str(app),
            algorithm="HS256"
        )

        return token

    def validate_token_status(self, token):
        """ Decodes a given token  """

        if SqlHelper().check_blacklisted_user_token(token):
            return "Token is no longer valid. Get a new one"

        try:
            data = jwt.decode(token, str(
                os.getenv("SECRET_KEY")), algorithms="HS256")

            return data["sub"]

        except jwt.ExpiredSignatureError:

            return "This token has already expired. Get a new one"

        except jwt.InvalidTokenError:

            return "This token is invalid"

    def check_authorization(self):
        """
        Checks for authorization
        and validates authentication token
        """

        header = request.headers.get("Authorization")

        if not header:
            return jsonify(
                {"error": "This resource is secured. Please provide authorization header",
                    "status": 400}
            ), 400

        auth_token = header.split(" ")[1]

        response = self.validate_token_status(auth_token)

        if isinstance(response, str):
            return jsonify(
                {"error": response,
                    "status": 400}
            ), 400

    def check_if_is_integer(self, data):
        """
        Check if the provided value for user key is an integer
        """

        try:
            if not isinstance(data["user"], int):
                return jsonify({"error": "Expected value for user to be an integer", "status": 400}), 400

        except KeyError as keyerr:
            return jsonify({"error": "Expected {} key to be present in the data but found none".format(keyerr), "status": 400}), 400
