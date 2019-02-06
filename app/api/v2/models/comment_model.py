from ....db_con import create_tables
from flask import current_app
from ..utils.sql_helpers import SqlHelper
from ..utils.validators import DataValidators
from datetime import datetime
from.base_model import BaseModels


class CommentModels(BaseModels):
    """
    This class CommentModels contain all the methods
    used to manipulate and handle comment and its
    details
    """

    def __init__(self, details={}):

        self.comment_details = details
        self.db = create_tables()
        self.sql = SqlHelper()

    def post_comment(self):
        """ Posts a comment to a question """

        locations = ["question_id", "user_id", "comments"]

        try:

            user = self.sql.get_username_by_id(
                int(self.comment_details["user"]))

            question = self.sql.fetch_details_by_criteria(
                "question_id", self.comment_details["question"], "questions")

            comment = self.comment_details["comment"]

            isempty = DataValidators(
                self.comment_details).check_values_not_empty()

            if isinstance(isempty, str):
                return self.makeresp(isempty, 400)

            if isinstance(comment, str):
                self.comment_details["comment"] = [comment]

        except KeyError as keyerror:
            return self.makeresp("{} is a required field".format(keyerror), 400)

        if not user:
            return self.makeresp("User not found", 404)

        if not question:
            return self.makeresp("Question not found", 404)

        comment_id = SqlHelper(self.comment_details).save_to_database(
            locations, "comments")

        return self.makeresp(
            {
                "id": comment_id,
                "user": user[0],
                "question": question[0][0],
                "title": question[0][3],
                "body": question[0][4],
                "comment": comment
            }, 201)

    def fetch_all_comments(self, question_id):
        """ Fetches all comments to questions """

        response = []

        comments = self.sql.get_all("comments", "question_id", question_id)

        for items in comments:

            user = self.sql.get_username_by_id(items[2])[0]

            response.append({
                "id": items[0],
                "createdBy": user,
                "question": items[1],
                "comment": items[3],
                "createdOn": items[4]

            })

        if not response:
            response = {
                "data": "No comments found to this question yet",
                "status": 200
            }

            return response

        return self.makeresp(response, 200)

    def fetch_one_comment(self, comment_id):
        """ Gets just one comment record with the passed id """

        comment_data = ''

        comment = self.sql.fetch_details_by_criteria(
            "comment_id", comment_id, "comments")

        if not comment:

            return self.makeresp("This comment cannot not be found", 404)

        user = self.sql.get_username_by_id(int(comment[0][2]))

        if len(comment[0][3]) == 1:

            comment_data = comment[0][3][0]

        response = self.makeresp({

            "user": user[0],
            "question": comment[0][1],
            "comment": comment_data,
            "createdOn": comment[0][4]
        }, 200)

        return response

    def remove_comment(self, comment_id):
        """ Removes a comment from the database """

        if not self.sql.fetch_details_by_criteria(
                "comment_id", comment_id, "comments"):

            return self.makeresp("This comment could not be found", 404)

        if not self.comment_details["user"] == self.sql.fetch_details_by_criteria(
                "comment_id", comment_id, "comments")[0][2]:

            return self.makeresp("You can not delete a comment you don't own", 403)

        SqlHelper().delete_from_database(comment_id, "comments")

        return self.makeresp({"message": "Comment deleted successfully"}, 200)
