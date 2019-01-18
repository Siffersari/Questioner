from flask import Flask
from instance.config import app_config
import os
from .api.v2.views.user_views import version2 as v2
from .api.v2.views.meetup_views import version2 as meets2
from .api.v2.views.question_views import version2 as ques2
from .api.v2.views.rsvp_views import version2 as rsvps2


def create_app(config_name="development"):

    app = Flask(__name__, instance_relative_config=True)
    app.url_map.strict_slashes = False
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    if config_name == "testing":
        os.environ["DATABASE_URL"] = os.getenv("DATABASE_TESTING_URL")

    app.register_blueprint(v2)
    app.register_blueprint(meets2)
    app.register_blueprint(ques2)
    app.register_blueprint(rsvps2)

    return app
