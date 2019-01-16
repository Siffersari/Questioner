from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from .base_model import BaseModels
from ..utils.validators import DataValidators
from flask import current_app
from .... db_con import create_tables
import re


class UserModels(BaseModels):
    """
    This class UserModels contains the methods used when
    interacting with user user
    """

    def __init__(self, details={}):
        self.user_details = details
        self.db = create_tables()

    def check_exists(self, email):
        """ Checks if the record exists """
        cur = self.db.cursor()

        cur.execute(
            """ SELECT email FROM users WHERE email = '%s';""" % (email))

        return cur.fetchone() is not None

    def register_user(self):
        """ Validates user user before adding them """

        required = ["firstname", "lastname", "othername",
                    "email", "phoneNumber", "username", "password"]

        ismissingkey = DataValidators(
            self.user_details).check_all_keys_present(required)

        if isinstance(ismissingkey, str):
            return self.makeresp(ismissingkey, 400)

        isempty = DataValidators(self.user_details).check_values_not_empty()

        if isinstance(isempty, str):
            return self.makeresp(isempty, 400)

        emailinvalid = DataValidators(self.user_details).check_email_is_valid()

        if not self.user_details["email"] == emailinvalid:
            return self.makeresp(emailinvalid, 400)

        isvalidpass = DataValidators(
            self.user_details).check_password_is_valid()

        if self.check_is_error(isvalidpass):
            return self.makeresp(isvalidpass, 400)

        if self.check_exists(self.user_details["email"]):

            return self.makeresp("This email already exists in the database", 409)

        payload = {
            "firstname": self.user_details["firstname"],
            "lastname": self.user_details["lastname"],
            "othername": self.user_details["othername"],
            "email": self.user_details["email"],
            "phoneNumber": self.user_details["phoneNumber"],
            "username": self.user_details["username"],
            "registered": datetime.now(),
            "password": generate_password_hash(self.user_details["password"]),
            "isAdmin": False
        }

        database = self.db
        cur = database.cursor()
        query = """INSERT INTO users (firstname, lastname, othername, email, phone_number, username, password) \
            VALUES ( %(firstname)s, %(lastname)s,\
            %(othername)s, %(email)s, %(phoneNumber)s, %(username)s, %(password)s) RETURNING user_id;
            """

        cur.execute(query, payload)
        user_id = cur.fetchone()[0]
        database.commit()
        cur.close()

        token = self.give_auth_token(user_id)

        token = token.decode('utf-8')

        resp = {
            "user": user_id,
            "name": "{} {}".format(payload["lastname"], payload["firstname"]),
            "token": token,
            "message": "You have been successfully registered"
        }

        return self.makeresp(resp, 201)

    def fetch_users(self):
        """ Returns all the users """

        database = self.db

        cur = database.cursor()
        cur.execute(
            """SELECT user_id, firstname, lastname FROM users;""")

        data = cur.fetchall()

        cur.close()

        resp = []

        for user in data:
            try:
                user_id, first_name, last_name = user
                final = {
                    "userId": user_id,
                    "user": "%s %s" % (last_name, first_name)
                }
                resp.append(final)
            except:
                pass

        return self.makeresp({
            "users": resp
        }, 200)


    def login_user(self):
        """ Logins in a user given correct user credentials """

        user = DataValidators(self.user_details).check_are_valid_credentials()

        status = 400

        if self.check_is_error(user):

            if "password" in user:

                status = 401

            return self.makeresp(user, status)

        user_id, firstname, lastname, password, registered = user

        token = self.give_auth_token(user_id)

        token = token.decode('utf-8')

        resp = {

            "name": "{} {}".format(lastname, firstname),
            "token": token,
            "message": "You have been logged in successfully"
        }

        return self.makeresp(resp, 200)