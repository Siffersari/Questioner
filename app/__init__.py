from flask import Flask, jsonify
from flask_cors import CORS
from instance.config import app_config
import os
from .api.v2.views.user_views import version2 as v2
from .api.v2.views.meetup_views import version2 as meets2
from .api.v2.views.question_views import version2 as ques2
from .api.v2.views.rsvp_views import version2 as rsvps2


def create_app(config_name="development"):

    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    app.url_map.strict_slashes = False
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    if config_name == "testing":
        os.environ["DATABASE_URL"] = os.getenv("DATABASE_TESTING_URL")

    app.register_blueprint(v2)
    app.register_blueprint(meets2)
    app.register_blueprint(ques2)
    app.register_blueprint(rsvps2)

    @app.errorhandler(400)
    def Badrequest(error):
        return jsonify({"error": "Bad Request. Please check that your input is valid", "status": 400}), 400

    @app.errorhandler(404)
    def NotFound(error):
        return jsonify({"error": "Not Found. The resource you are trying to access was not found", "status": 404}), 404

    @app.errorhandler(405)
    def Notallowed(error):
        return jsonify({"error": "This method is not allowed on this resource", "status": 405}), 405

    @app.errorhandler(500)
    def ServerError(error):
        return jsonify({"error": "Internal error", "status": 500}), 500

    return app 
