from flask import Flask, request
from .. import version1
from .. models.user_model import UserModels

db = UserModels()


@version1.route("/", methods=["GET"])
def hello():
    """ Returns 'hello world' """
    return "hello world"

    