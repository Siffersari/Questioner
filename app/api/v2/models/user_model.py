from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from .base_model import BaseModels
from ..utils.validators import DataValidators
from ..utils.sql_helpers import SqlHelper
from flask import current_app, url_for, Flask
from flask_mail import Mail, Message
from .... db_con import create_tables
import re
import os


app = Flask(__name__)

app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT') or 25)
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS') is not None
app.config['MAIL_USE_SSL'] = os.environ.get('MAIL_USE_SSL') is not None
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

mail = Mail(app)


class UserModels(BaseModels):
    """
    This class UserModels contains the methods used when
    interacting with user user
    """

    def __init__(self, details={}):
        self.user_details = details
        self.db = create_tables()

    def register_user(self):
        """ Validates user user before adding them """

        locations = ["firstname", "lastname", "othername",
                     "email", "phone_number", "username", "password"]

        required = ["firstname", "lastname", "othername",
                    "email", "phoneNumber", "username", "password"]

        phone = self.user_details["phoneNumber"]

        if not (str(phone).isdigit() and len(phone) == 10):

            return self.makeresp("Please ensure that your phone number is valid", 400)

        try:

            if self.user_details["password"] != self.user_details["confirmPass"]:

                return self.makeresp("Please ensure that both password fields match", 400)
        except KeyError as keyismis:
            return self.makeresp("Expected {} in data provided, instead got none".format(keyismis), 400)

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

        if SqlHelper().check_user_exist_by_email(self.user_details["email"]):

            return self.makeresp("This email already exists in the database", 409)

        if not isinstance(SqlHelper().get_user_by_username(self.user_details["username"]), str):

            return self.makeresp("This username already exists in the database", 409)

        payload = {
            "firstname": self.user_details["firstname"],
            "lastname": self.user_details["lastname"],
            "othername": self.user_details["othername"],
            "email": self.user_details["email"],
            "phoneNumber": self.user_details["phoneNumber"],
            "username": self.user_details["username"],
            "password": generate_password_hash(self.user_details["password"])
        }

        user_id = SqlHelper(payload).save_to_database(locations, "users")

        token = self.give_auth_token(user_id)

        token = token.decode('utf-8')

        resp = {
            "user": user_id,
            "name": "{} {}".format(payload["lastname"], payload["firstname"]),
            "token": token,
            "message": "You have been successfully registered"
        }

        return self.makeresp(resp, 201)

    def fetch_user(self, user_id):
        """ Returns all the users """

        user = SqlHelper().get_user(user_id)

        questions = SqlHelper().fetch_statistics(user_id, "questions")

        comments = SqlHelper().fetch_statistics(user_id, "comments")

        return self.makeresp({
            "name": "{} {}".format(user[2], user[1]),
            "email": user[4],
            "phoneNumber": user[5],
            "username": user[6],
            "registeredOn": user[7],
            "isAdmin": user[9],
            "questions": questions[0],
            "comments": comments[0]
        }, 200)

    def login_user(self):
        """ Logins in a user given correct user credentials """

        user = DataValidators(self.user_details).check_are_valid_credentials()

        status = 404

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

    def logout_user(self, token):
        """ Blacklists a user's token """

        details = {
            "token": token
        }

        blacked_token = SqlHelper(details).save_to_database('', "blacklist")

        return self.makeresp({"message": "You have been successfully logged out",
                              "status": 200,
                              "token": blacked_token}, 200)

    def request_password_reset(self, email):
        """ Sends password reset email if email exists """

        user = SqlHelper().check_user_exist_by_email(email)

        if not user:
            return self.makeresp("This email doesn't not exist", 400)

        token = UserModels().give_auth_token(email=email)

        message = Message('Password Reset',
                          sender=os.environ.get('MAIL_USERNAME'), recipients=[email])

        link = url_for('version2.reset_password',
                       token=token.decode('utf-8'), _external=True)

        message.body = 'Your reset password link {}'.format(link)

        try:
            mail.send(message)

        except Exception as exception:

            return {
                "message": "This request could not be completed",
                "status": 422,
                "error": str(exception)
            }

        return {

            "message": 'Please check your email for instructions',
            "status": 200
        }

    def reset_password(self):
        """ Resets the existing password """

        try:

            match = self.user_details["password"] == self.user_details["confirmPass"]

            if not match:

                return self.makeresp("Please ensure that both password fields match", 400)

        except KeyError as misskey:

            return self.makeresp("Expected {} in data provided, instead got none".format(misskey), 400)

        isempty = DataValidators(self.user_details).check_values_not_empty()

        if self.check_is_error(isempty):

            return self.makeresp(isempty, 400)

        password = generate_password_hash(self.user_details["password"])

        email = SqlHelper().update_password(
            password, self.user_details["email"])

        if not email:

            return self.makeresp("This action has been forbidden", 403)

        response = {
            "message": "Password reset successfully",
            "status": 200,
            "email": email[0]
        }

        return self.makeresp(response, 200)
