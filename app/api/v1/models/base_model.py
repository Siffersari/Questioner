# These 4 list store data for users, meetups, questions & rsvps respectively

users, meetups, questions, rsvps = [], [], [], []


class BaseModels(object):
    """ 
    This class contains methods that are common to all other
    models
    """

    def __init__(self):
        self.users = users
        self.meetups = meetups
        self.questions = questions
        self.rsvps = rsvps

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

    def check_item_exists(self, key, item, database):
        """ 
        This method accepts a key e.g username
        an item e.g 'Leewel' and
        a database e.g users 
        """
        # if database = user ... try check for with 'index of where it is found'

        # Confirm if all databases store in a similar structure

        # example for user
        try:
            data = [record for record in database if record[key].lower() == item.lower()]
        except:
            data = [record for record in database if record[key] == int(item)]
        if not data:
            return "{} not found".format(key)

        return data


    def check_item_return_index(self, key, item, database):
        """ 
        This method accepts a key e.g username, an item which is being 
        checked for e.g 'Leewel' and a database to search for the item
        e.g users
        """

        try:
            data = [[ind, record] for [ind, record] in enumerate(database) if record[key].lower() == item.lower()]

        except:
            data = [[ind, record] for [ind, record] in enumerate(database) if record[key] == int(item)]

        if not data:
            return "{} not found".format(key)

        return data


    def check_missing_details(self, details):
        """ 
        Checks if required data exists in the provided details
        and returns missing values or [] if none
        """
        
        for key, value in details.items():
            if not value:
                return "{} is a required field".format(key)


    def check_is_error(self, data):
        """ Checks if data passed to it is of type string """

        return isinstance(data, str)
            