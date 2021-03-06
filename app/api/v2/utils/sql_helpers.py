from flask import current_app
from ....db_con import create_tables


class SqlHelper:
    """
    This class SqlHelper contains all
    methods for executing SQL statements
    """

    def __init__(self, details={}):

        self.database = create_tables()
        self.details = details

    def get_all(self, database, item_name='', item_id=''):
        """
        Fetches all details from a specified
        database
        """

        cur = self.database.cursor()

        if item_id:

            cur.execute(
                """ SELECT * FROM {} WHERE {} = {} ;""".format(database, item_name, item_id))

        elif database == "questions" and not item_id:

            cur.execute(
                """ SELECT * FROM {} ORDER BY votes DESC;""".format(database))

        elif database == "comments" and not item_id:

            cur.execute(""" SELECT * FROM {};""".format(database))

        all_items = cur.fetchall()

        cur.close()

        return all_items

    def fetch_details(self, item, database, item_name, item_id):
        """
        Fetches requested data from the specified
        database
        """

        cur = self.database.cursor()

        query = """ SELECT {} FROM {} WHERE {} = {} ;"""

        if database == 'rsvps':

            query = """ SELECT {} FROM {} WHERE {} = {} AND response = 'yes' ;"""

        cur.execute(query.format(item, database, item_name, item_id))

        all_items = cur.fetchall()

        cur.close()

        return all_items or 'None'

    def get_admin_user(self, user_id):
        """ Fetches admin user if exists """

        cur = self.database.cursor()

        cur.execute(
            """ SELECT user_id FROM users WHERE roles = 'true'; """)

        admins = cur.fetchall()

        cur.close()

        if not admins:
            return "Administrators not Found"

        admin = [user for user in admins if user_id in user]

        try:

            if not int(user_id) in admin[0]:
                return "This user doesn't have the priviledges for this action."

        except:

            return "This user doesn't have the priviledges for this action."

        return user_id

    def make_user_administrator(self, user_id):
        """ Checks if a user is an admin using the user_id """

        cur = self.database.cursor()
        cur.execute(
            """ UPDATE users SET roles = true WHERE user_id = %d RETURNING roles; """ % (int(user_id)))

        admins = cur.fetchone()

        self.database.commit()

        cur.close()

        if not admins:
            return "Failed to add user as Admin"

        return admins

    def fetch_rsvp(self, meetup_id):
        """ Returns all the rsvps with the given meetup id """

        try:
            cur = self.database.cursor()
            cur.execute(
                """ SELECT user_id, response FROM rsvps WHERE meetup_id = {}; """.format(meetup_id))

            data = cur.fetchall()

            cur.close()

            return data

        except Exception:
            return "Not Found"

    def fetch_details_by_criteria(self, item_name, criteria, table):
        """ returns details of any matching criteria given """

        try:
            cur = self.database.cursor()
            if isinstance(criteria, str):
                cur.execute(
                    """ SELECT * FROM {} WHERE {} = '{}'; """.format(table, item_name, criteria))
            else:
                cur.execute(
                    """ SELECT * FROM {} WHERE {} = {}; """.format(table, item_name, criteria))

            data = cur.fetchall()

            cur.close()

            return data

        except Exception:
            return "Not Found"

    def fetch_details_if_text_exists(self, item_name, text, table):

        cur = self.database.cursor()
        cur.execute(""" SELECT * FROM %s WHERE lower(%s) = '%s'; """ % (
            table, item_name, text.lower().replace("'", "''")))

        text = cur.fetchall()

        if not text:

            return " Text not found"

        return text

    def get_username_by_id(self, user_id):
        """ returns a username given the id """

        try:
            cur = self.database.cursor()
            cur.execute(
                """ SELECT username FROM users WHERE user_id = %d;""" % (user_id))
            username = cur.fetchone()
            cur.close()

            return username

        except Exception:
            return "Not Found"

    def get_user_by_username(self, username):
        """ Fetches a user's details from the database given a username """

        cur = self.database.cursor()
        cur.execute(
            """ SELECT user_id ,firstname, lastname, password, registered_on FROM users WHERE username = '{}'; """.format(username))

        user_details = cur.fetchone()

        cur.close()

        if not user_details:
            return "User not Found"

        return user_details

    def check_blacklisted_user_token(self, token):
        """ Accepts a token and checks validity """

        curr = self.database.cursor()

        query = """ SELECT * FROM blacklist WHERE tokens = %s; """

        curr.execute(query, [token])

        blacklisted = curr.fetchone()

        if blacklisted:
            return True

        return False

    def save_to_database(self, locations, database):
        """
        accepts the column names as location 
        and a database name to save the data into
        and saves the data to the specified database
        """

        queries = {
            "meetup": """ %(createdBy)s, %(topic)s, %(location)s, %(happeningOn)s, %(images)s, %(Tags)s """,
            "user": """ %(firstname)s, %(lastname)s, %(othername)s, %(email)s, %(phoneNumber)s, %(username)s, %(password)s """,
            "question": """ %(meetup)s, %(createdBy)s, %(title)s, %(body)s """,
            "rsvp": """ %(user)s, %(meetup)s, %(response)s """,
            "comment": """ %(question)s, %(user)s, %(meetup)s, %(comment)s """,
            "vote": """ %(question)s, %(user)s, %(meetup)s, %(vote)s """,
            "blacklis": """ %(token)s """
        }

        table_key = database[:-1]

        item_id, values = table_key + '_id', queries[table_key]

        columns = ", ".join(locations)

        cur = self.database.cursor()

        query = """ INSERT INTO %s (%s) VALUES (%s) RETURNING %s; """ % (
            database, columns, values, item_id)

        if database == "blacklist":

            query = """ INSERT INTO blacklist VALUES (%s) RETURNING tokens; """ % (
                values)

        cur.execute(query, self.details)

        required_id = cur.fetchone()[0]

        self.database.commit()

        cur.close()

        return required_id

    def vote_question(self, question_id, vote="up"):
        """ Up or down votes an answer """

        cur = self.database.cursor()

        number_votes = """ SELECT votes FROM questions WHERE question_id = {}; """.format(
            question_id)

        cur.execute(number_votes)

        votes_num = cur.fetchone()[0]

        if vote == "down":
            if votes_num == 0:
                updated = 0
            else:
                updated = votes_num - 1

        else:
            updated = votes_num + 1

        query = """ UPDATE questions SET votes = {} WHERE question_id = {} RETURNING meetup_id, title, body, votes; """.format(
            updated, question_id)

        cur.execute(query)

        data = cur.fetchone()

        self.database.commit()

        cur.close()

        return data

    def update_votes(self, vote_id, status):
        """ Updates the vote to either upvote or downvote """

        cur = self.database.cursor()

        query = """ UPDATE votes SET vote = '{}' WHERE vote_id = {} RETURNING vote; """.format(
            status, vote_id)

        cur.execute(query)

        data = cur.fetchone()

        self.database.commit()

        cur.close()

        return data

    def get_upcoming_meetups(self):

        cur = self.database.cursor()
        cur.execute(""" SELECT * FROM meetups WHERE happening_on > now(); """)
        meetups = cur.fetchall()
        cur.close()

        return meetups

    def delete_from_database(self, item_id, database, option_name=""):
        """ Deletes a meetup record """

        table_key = database[:-1]

        item_name = table_key + '_id'

        cur = self.database.cursor()

        if option_name:
            item_name = option_name

        try:
            cur.execute(
                """ DELETE FROM %s WHERE %s = %d; """ % (database, item_name, item_id))

            self.database.commit()

        except:
            return False

        return "Meetup deleted successfully"

    def check_user_exist_by_email(self, email):
        """ Checks database for existing users using user emails """

        cur = self.database.cursor()

        cur.execute(
            """ SELECT email FROM users WHERE lower(email) = '%s';""" % (email.lower()))

        email = cur.fetchone()

        return email

    def get_user(self, user_id):
        """ 
        Returns all the users details from the database associated with the given user id
        """

        cur = self.database.cursor()

        cur.execute(
            """SELECT * FROM users WHERE user_id = {};""".format(user_id))

        user = cur.fetchone()

        if not user:

            return "User not Found"

        cur.close()

        return user

    def fetch_statistics(self, user_id, database):
        """ Fetches user statistics from database """

        cur = self.database.cursor()

        cur.execute(
            """ SELECT COUNT (*) FROM %s WHERE user_id = %d;""" % (database, user_id))

        data = cur.fetchone()

        if not data:

            return 'None yet'

        return data

    def get_images(self, meetup_id):
        """ Fetches images from the database """

        cur = self.database.cursor()

        cur.execute(""" SELECT images FROM meetups WHERE meetup_id = %d; """ % (
            meetup_id))

        images = cur.fetchone()[0]

        cur.close()

        if not images:
            return "Images not found"

        return images

    def post_images(self, meetup_id):
        """ Saves images to the database """

        data = {
            "images": self.details["images"],
            "meetupId": meetup_id
        }

        cur = self.database.cursor()

        query = """ UPDATE meetups SET images = %(images)s WHERE meetup_id = %(meetupId)s RETURNING images; """

        cur.execute(query, data)

        images = cur.fetchone()[0]

        self.database.commit()

        cur.close()

        return images

    def get_tags(self, meetup_id):
        """ Fetches the tags to a meetup from the database """

        cur = self.database.cursor()

        query = """ SELECT tags FROM meetups WHERE meetup_id = %d; """ % (
            meetup_id)

        cur.execute(query)

        tags = cur.fetchone()[0]

        cur.close()

        if not tags:
            return "Tags not found"

        return tags

    def add_tags(self, meetup_id):
        """ Saves tags to a meetup in the database """

        data = dict(
            tags=self.details["tags"],
            meetupId=meetup_id
        )

        cur = self.database.cursor()

        query = """ UPDATE meetups SET tags = %(tags)s WHERE meetup_id = %(meetupId)s RETURNING images; """

        cur.execute(query, data)

        tags = cur.fetchone()[0]

        self.database.commit()

        cur.close()

        return tags

    def update_password(self, password, email):
        """ Updates the password field """

        cur = self.database.cursor()

        cur.execute(""" UPDATE users SET password = '{}' WHERE lower(email) =  '{}' RETURNING email; """.format(
            password, email.lower()))

        email = cur.fetchone()

        self.database.commit()

        cur.close()

        return email
