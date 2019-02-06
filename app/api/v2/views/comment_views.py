from flask import Flask, request, jsonify, make_response
from .. import version2
from .. models.comment_model import CommentModels


@version2.route("/comments", methods=["POST"])
def post_comment():
    """ Posts a comment to a question """

    details, not_authorized = request.get_json(), CommentModels().check_authorization()

    if not isinstance(not_authorized, int):

        return not_authorized

    details["user"] = not_authorized

    resp = CommentModels(details).post_comment()

    return make_response(jsonify(resp), resp["status"])


@version2.route("/questions/<int:question_id>/comments", methods=['GET'])
def fetch_all_comments(question_id):
    """ Fetches all comments to a question """

    if not isinstance(CommentModels().check_authorization(), int):

        return CommentModels().check_authorization()

    return make_response(jsonify(CommentModels().fetch_all_comments(question_id)), 200)


@version2.route("/comments/<int:comment_id>", methods=["GET"])
def fetch_one_comment(comment_id):
    """ Returns the comment given the id """

    if not isinstance(CommentModels().check_authorization(), int):

        error_response = CommentModels().check_authorization()

        return error_response

    response = CommentModels().fetch_one_comment(comment_id)

    status = response["status"]

    return jsonify(response), status


@version2.route("/comments/<int:comment_id>", methods=['DELETE'])
def delete_comment(comment_id):
    """ Deletes a comment to a question if exists by Id """

    decoded_auth = CommentModels().check_authorization()

    if not isinstance(decoded_auth, int):

        return decoded_auth

    details = {
        "user": decoded_auth
    }

    result = CommentModels(details).remove_comment(comment_id)

    return jsonify(result), result["status"]
