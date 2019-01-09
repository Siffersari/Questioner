from datetime import datetime
from werkzeug.security import generate_password_hash
# This array users, store all the registered users

users = []


class UserModels(object):
    """
    This class UserModels contains the methods used when 
    interacting with user user
    """

    def __init__(self):
        self.db = users

    def makeresp(self, payload, status_code):
        """ Returns user if found and message if not """
        if isinstance(payload, str):
            return {
                "status": status_code,
                "error": payload
            }

        return {
            "status": status_code,
            "data": [payload]
        }

    def register_user(self, user):

        """ Validates user user before adding them """

        import re
        for key, value in user.items():
            if not value:
                return self.makeresp("{} is a required field.".format(key), 400)

            if (key == 'email' and not re.search(r'\w+[.|\w]\w+@\w+[.]\w+[.|\w+]\w+', value)):
                return self.makeresp("Please enter a valid {}.".format(key), 400)

            if (key == 'fName' or key == 'lName' or key == 'uname') and (len(value) < 4 or len(value) > 15):
                return self.makeresp("{} should be 4-15 characters long".format(key), 400)

            if key == 'password':

                if not (len(re.findall(r'[A-Z]', value)) > 0 and len(re.findall(
                        r'[a-z]', value)) > 0 and len(re.findall(r'[0-9]', value)) > 0 and len(re.findall(r'[@#$]', value)) > 0):

                    return self.makeresp("{} should contain atleast one number, uppercase, lowercase and special character".format(key), 400)
        payload = {
            "id": len(self.db) + 1,
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

        self.db.append(payload)

        resp = {
            "id": payload["id"],
            "name": "{} {}".format(payload["lastname"], payload["firstname"])
        }

        return self.makeresp(resp, 201)

    
    def fetch_users(self):
        """ Returns all the users """
        resp = {
            "users": self.db
        }
        return self.makeresp(resp, 200)

        
