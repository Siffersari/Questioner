from flask import Flask
from instance.config import app_config

from .api.v1.views.user_views import version1 as v1
from .api.v1.views.meetup_views import version1 as meets
from .api.v1.views.question_views import version1 as ques
from .api.v1.views.rsvp_views import version1 as rsvps


def create_app(config_name="development"):
    app = Flask(__name__, instance_relative_config=True)
    app.url_map.strict_slashes = False
    app.config.from_object(app_config["development"])
    app.config.from_pyfile('config.py')

    app.register_blueprint(v1)
    app.register_blueprint(meets)
    app.register_blueprint(ques)
    app.register_blueprint(rsvps)

    return app
