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

    def get_admin_user(self, user_id):
        """ Fetches admin user if exists """

        cur = self.database.cursor()

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

        cur = self.database.cursor()
        cur.execute(
            """ UPDATE users SET roles = true WHERE user_id = %d RETURNING roles; """ % (int(user_id)))

        admins = cur.fetchone()

        self.database.commit()

        cur.close()

        if not admins:
            return "Failed to add user as Admin"

        return admins

    def fetch_details_by_id(self, item_name, item_id, table):
        """ returns a details given the id """

        try:
            cur = self.database.cursor()
            cur.execute(
                """ SELECT * FROM {} WHERE {} = {}; """.format(table, item_name, int(item_id)))

            data = cur.fetchone()

            cur.close()

            #response = [item for item in data if item in required]

            return data

        except Exception:
            return "Not Found"

    def fetch_id_if_text_exists(self, item_name, text, table):
        # select meetup_id from meetups where topic = 'This is topic';
        singular = table[:-1] + '_id'

        cur = self.database.cursor()
        cur.execute(""" SELECT {} FROM {} WHERE lower({}) = '{}'; """.format(
            singular, table, item_name, text.lower()))
        text = cur.fetchone()

        if not text:
            # no meetup or question found with that text
            return " Text not found"

        return text[0]

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

        query = """ SELECT * FROM blacklisted WHERE tokens = %s; """

        curr.execute(query, [token])

        blacklisted = curr.fetchone()

        if blacklisted:
            return True

        return False

    def save_meetup(self):
        """ Saves question to the database """

        cur = self.database.cursor()
        query = """ INSERT INTO meetups (user_id, topic, location, happening_on, images, tags) VALUES (%(createdBy)s, %(topic)s, %(location)s, %(happeningOn)s, %(images)s, %(Tags)s) RETURNING meetup_id; """
        cur.execute(query, self.details)

        meetup_id = cur.fetchone()[0]
        self.database.commit()
        cur.close()

        return meetup_id

    def get_upcoming_meetups(self):

        cur = self.database.cursor()
        cur.execute(""" SELECT * FROM meetups WHERE happening_on > now(); """)
        meetups = cur.fetchall()
        cur.close()

        return meetups

    def delete_meetup(self, meetup_id):
        """ Deletes a meetup record """

        cur = self.database.cursor()

        try:
            cur.execute(
                """ DELETE FROM meetups WHERE meetup_id = %d; """ % (meetup_id))

            self.database.commit()

        except:
            return False

        return "Meetup deleted successfully"

    def check_user_exist_by_email(self, email):
        """ Checks database for existing users using user emails """

        cur = self.database.cursor()

        cur.execute(
            """ SELECT email FROM users WHERE email = '%s';""" % (email))

        return cur.fetchone() is not None

    def save_user(self):
        """ Adds user details to the database """

        cur = self.database.cursor()
        query = """INSERT INTO users (firstname, lastname, othername, email, phone_number, username, password) \
            VALUES ( %(firstname)s, %(lastname)s,\
            %(othername)s, %(email)s, %(phoneNumber)s, %(username)s, %(password)s) RETURNING user_id;
            """

        cur.execute(query, self.details)
        user_id = cur.fetchone()[0]
        self.database.commit()
        cur.close()

        return user_id

    def get_all_users(self):
        """ Returns all the users in the database """

        cur = self.database.cursor()

        cur.execute(
            """SELECT user_id, firstname, lastname FROM users;""")

        users = cur.fetchall()

        cur.close()

        return users

    def save_question(self):
        """ Adds question to the database """

        cur = self.database.cursor()
        query = """ INSERT INTO questions (meetup_id, user_id, title, body) VALUES (%(createdBy)s, %(meetup)s, %(title)s, %(body)s) RETURNING question_id; """
        cur.execute(query, self.details)

        question_id = cur.fetchone()[0]
        self.database.commit()
        cur.close()

        return question_id

    def upvote_question(self, question_id):
        """ Upvotes a question """

        cur = self.database.cursor()
        query = """ UPDATE questions SET votes = votes + 1 WHERE question_id = {} RETURNING meetup_id, title, body, votes; """.format(
            question_id)
        cur.execute(query)

        data = cur.fetchone()
        self.database.commit()
        cur.close()

        return data

    def downvote_question(self, question_id):
        """ Upvotes a question """

        cur = self.database.cursor()
        query = """ UPDATE questions SET votes = votes - 1 WHERE question_id = {} RETURNING meetup_id, title, body, votes; """.format(
            question_id)
        cur.execute(query)

        data = cur.fetchone()
        self.database.commit()
        cur.close()

        return data

    def reply_meetup(self, rsvp):
        """ Saves attendance response to the database """

        cur = self.database.cursor()
        query = """ INSERT INTO rsvps (user_id, meetup_id, response) VALUES (%(user)s, %(meetup)s, %(response)s) RETURNING rsvp_id; """
        cur.execute(query, rsvp)

        rsvp_id = cur.fetchone()[0]
        self.database.commit()
        cur.close()

        return rsvp_id

    def save_comment(self):
        """ Save comment details to the database """

        cur = self.database.cursor()

        query = """ INSERT INTO comments (question_id, user_id, comments) VALUES (%(question)s, %(user)s, %(comment)s) RETURNING comment_id; """
        cur.execute(query, self.details)

        comment_id = cur.fetchone()[0]
        self.database.commit()
        cur.close()

        return comment_id
