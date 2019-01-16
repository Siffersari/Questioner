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

    def get_user_by_username(self, username):
        """ Fetches a user's details from the database given a username """

        database = create_tables()

        cur = database.cursor()
        cur.execute(
            """ SELECT user_id ,firstname, lastname, password, registered_on FROM users WHERE username = '{}'; """.format(username))

        data = cur.fetchone()

        cur.close()

        if not data:
            return "User not Found"

        return data

    def get_username_by_id(self, user_id):
        """ returns a username given the id """

        try:
            cur = create_tables().cursor()
            cur.execute(
                """ SELECT username FROM users WHERE user_id = %d;""" % (user_id))
            data = cur.fetchone()
            cur.close()

            return data

        except Exception:
            return "Not Found"

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
            "exp": datetime.utcnow() + timedelta(days=1),
            "iat": datetime.utcnow(),
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

    def check_user_is_admin(self, user_id):
        """ Checks if a user is an admin using the user_id """
        database = create_tables()

        cur = database.cursor()
        cur.execute(
            """ SELECT user_id FROM users WHERE roles = 'true'; """)

        admins = cur.fetchall()

        cur.close()

        if not admins:
            return "Administrators not Found"

        if not int(user_id) in admins[0]:
            return "This user doesn't have the priviledges for this action"

        return user_id

    def make_user_administrator(self, user_id):
        """ Checks if a user is an admin using the user_id """
        database = create_tables()

        cur = database.cursor()
        cur.execute(
            """ UPDATE users SET roles = true WHERE user_id = %d RETURNING roles; """ % (int(user_id)))

        admins = cur.fetchone()

        database.commit()

        cur.close()

        if not admins:
            return "Failed to add user as Admin"

        return admins
