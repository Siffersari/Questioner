from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from .common_model import CommonModels
from werkzeug.exceptions import BadRequest, NotFound, Unauthorized


class UserModels(CommonModels):
    """
    This class UserModels contains the methods used when 
    interacting with user user
    """

    def register_user(self, user):
        """ Validates user user before adding them """

        import re
        for key, value in user.items():
            if not value:
                raise BadRequest("{} is a required field.".format(key))

            if (key == 'email' and not re.search(r'\w+[.|\w]\w+@\w+[.]\w+[.|\w+]\w+', value)):
                raise BadRequest("Please enter a valid {}.".format(key))

            if (key == 'firstname' or key == 'lastname' or key == 'username') and (len(value) < 4 or len(value) > 15):
                raise BadRequest(
                    "{} should be 4-15 characters long".format(key))

            if key == 'password':

                if not (len(re.findall(r'[A-Z]', value)) > 0 and len(re.findall(
                        r'[a-z]', value)) > 0 and len(re.findall(r'[0-9]', value)) > 0 and len(re.findall(r'[@#$]', value)) > 0):

                    raise BadRequest(
                        "{} should contain atleast one number, uppercase, lowercase and special character".format(key))
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

    def login_user(self, username, password):
        """ Logins in a user given correct user credentials """

        user = self.check_item_exists("username", username, self.users)

        if isinstance(user, str):

            raise NotFound("Please check your username")

        if not check_password_hash(user[0]["password"], password):

            raise Unauthorized("Please check your password")

        resp = {

            "name": "{} {}".format(user[0]["lastname"], user[0]["firstname"]),
            "memberSince": "{:%B %d, %Y}".format(user[0]["registered"]),
            "message": "You have been logged in successfully"
        }

        return self.makeresp(resp, 200)
