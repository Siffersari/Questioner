import os
from ....db_con import create_tables
from flask import current_app
from datetime import datetime, timedelta
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

    def fetch_id_if_text_exists(self, item_name, text, table):
        # select meetup_id from meetups where topic = 'This is topic';
        singular = table[:-1] + '_id'

        cur = create_tables().cursor()
        cur.execute(""" SELECT {} FROM {} WHERE lower({}) = '{}'; """.format(
            singular, table, item_name, text.lower()))
        data = cur.fetchone()

        if not data:
            # no meetup or question found with that text
            return " Text not found"

        return data[0]

    def fetch_details_by_id(self, item_name, item_id, table):
        """ returns a username given the id """

        try:
            cur = create_tables().cursor()
            cur.execute(
                """ SELECT * FROM {} WHERE {} = {}; """.format(table, item_name, int(item_id)))
            data = cur.fetchone()
            cur.close()

            #response = [item for item in data if item in required]

            return data

        except Exception:
            return "Not Found"

    def check_is_error(self, data):
        """ Checks if data passed to it is of type string """

        return isinstance(data, str)

    @staticmethod
    def give_auth_token(user_id):
        """ Generates a JWT auth token """
        app = os.getenv("SECRET_KEY")
 

        token_data = {
            "exp": datetime.now() + timedelta(days=1),
            "iat": datetime.now(),
            "sub": user_id
        }

        token = jwt.encode(
            token_data,
            app,
            algorithm="HS256"
        )

        return token

    def check_blacklisted_user_token(self, token):
        """ Accepts a token and checks validity """

        dbconn = create_tables()

        curr = dbconn.cursor()

        query = """ SELECT * FROM blacklisted WHERE tokens = %s; """

        curr.execute(query, [token])

        blacklisted = curr.fetchone()

        if blacklisted:
            return True

        return False

    def validate_token_status(self, token):
        """ Decodes a given token """

        if self.check_blacklisted_user_token(token):
            return "Token is no longer valid. Get a new one"

        try:
            data = jwt.decode(token, os.getenv("SECRET_KEY"))

            return data["sub"]

        except jwt.ExpiredSignatureError:

            return "This token has already expired. Get a new one"

        except jwt.InvalidTokenError:

            return "This token is invalid"
