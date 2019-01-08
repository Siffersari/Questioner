from flask import Flask


def create_app():
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    
    return app 