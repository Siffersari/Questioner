from ..models.base_model import BaseModels
from ..utils.sql_helpers import SqlHelper
import re
from werkzeug.security import generate_password_hash, check_password_hash


class DataValidators(BaseModels):
    """ 
    This class DataValidators contain all them methods that
    validate data all across the applfrom werkzeug.security import generate_password_hash, check_password_hashfrom werkzeug.security import generate_password_hash, check_password_hashication
    """

    def __init__(self, data={}):
        self.given_data = data

    def check_all_keys_present(self, required):
        """ 
        This method takes in a list of required fields and a
        dictionary with the required data and returns the missing
        data if any or list of items found
        """

        missing = [key for key in required
                   if not key in self.given_data.keys()]

        if missing:
            return "{} is a required key in the data provided".format(missing[0])

        return required

    def check_values_not_empty(self):
        """ 
        This method accepts data in form of a 
        dictionary and checks that the value is not 
        empty and returns the key if empty
        """

        missing = []

        for key, value in self.given_data.items():
            if not (key == "images") and not value:
                missing.append(key)

        if missing:
            return "{} is a required field".format(missing[0])

        return self.given_data

    def check_email_is_valid(self):
        """ Takes in an email and checks whether or not it is valid """

        if not re.search(r'\w+[.|\w]\w+@\w+[.]\w+[.|\w+]\w+', self.given_data["email"]) or re.search(r'\s', self.given_data["email"]):
            return "Please enter a valid email address"

        return self.given_data["email"]

    def check_password_is_valid(self):
        password = self.given_data["password"]

        upper_case, lower_case = len(re.findall(
            r'[A-Z]', password)), len(re.findall(r'[a-z]', password))

        digits = re.findall(
            r'[0-9]', password)

        special = len(re.findall(r'[@#$]', password))

        if not (upper_case and lower_case and len(digits) and special) > 0:

            return "Password should contain atleast one number, uppercase, lowercase and special character"

    def check_are_valid_credentials(self):
        """ Checks if the provided credentials match the ones registered """

        user = SqlHelper().get_user_by_username(self.given_data["username"])

        if isinstance(user, str):

            return "Please check your username"

        user_id, firstname, lastname, password, registered = user

        if not check_password_hash(password, self.given_data["password"]):

            return "Please check your password "
        return user
