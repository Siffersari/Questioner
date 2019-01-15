from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from .base_model import BaseModels
from ..utils.validators import DataValidators
from werkzeug.exceptions import BadRequest, NotFound, Unauthorized
import re


class UserModels(BaseModels):
    """
    This class UserModels contains the methods used when
    interacting with user user
    """

    def register_user(self, user):
        """ Validates user user before adding them """

        required = ["firstname", "lastname", "othername",
                    "email", "phoneNumber", "username", "password"]

        ismissingkey = DataValidators(user).check_all_keys_present(required)

        if isinstance(ismissingkey, str):
            return self.makeresp(ismissingkey, 400)

        isempty = DataValidators(user).check_values_not_empty()

        if isinstance(isempty, str):
            return self.makeresp(isempty, 400)

        emailinvalid = DataValidators(user).check_email_is_valid()

        if not user["email"] == emailinvalid:
            return self.makeresp(emailinvalid, 400)

        isvalidpass = DataValidators(user).check_password_is_valid()

        if self.check_is_error(isvalidpass):
            return self.makeresp(isvalidpass, 400)

        userFound = self.check_item_exists("email", user["email"], self.users)

        if not isinstance(userFound, str):
            return self.makeresp("This email already exists in the database", 409)

        payload = {
            "id": len(self.users) + 1,
            "firstname": user["firstname"],
            "lastname": user["lastname"],
            "othername": user["othername"],
            "email": user["email"],
            "phoneNumber": user["phoneNumber"],
            "username": user["username"],
            "registered": datetime.now(),
            "password": generate_password_hash(user["password"]),
            "isAdmin": False
        }

        self.users.append(payload)

        resp = {
            "id": payload["id"],
            "name": "{} {}".format(payload["lastname"], payload["firstname"])
        }

        return self.makeresp(resp, 201)

    def fetch_users(self):
        """ Returns all the users """

        return self.makeresp({
            "users": self.users
        }, 200)

    def login_user(self, data):
        """ Logins in a user given correct user credentials """

        user = DataValidators(data).check_are_valid_credentials()

        status = 400

        if self.check_is_error(user):

            if "password" in user:

                status = 401

            return self.makeresp(user, status)

        resp = {

            "name": "{} {}".format(user[0]["lastname"], user[0]["firstname"]),
            "memberSince": "{:%B %d, %Y}".format(user[0]["registered"]),
            "message": "You have been logged in successfully"
        }

        return self.makeresp(resp, 200)
