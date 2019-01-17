import os
from flask import current_app
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
        """ Decodes a given token """

        if SqlHelper().check_blacklisted_user_token(token):
            return "Token is no longer valid. Get a new one"

        try:
            data = jwt.decode(token, os.getenv("SECRET_KEY"))

            return data["sub"]

        except jwt.ExpiredSignatureError:

            return "This token has already expired. Get a new one"

        except jwt.InvalidTokenError:

            return "This token is invalid"
