# This file config, contains different settings of the application
# to suite the intended purpose. 

import os

class Config(object):
    DEBUG = False
    SECRET_KEY = os.getenv("SECRET_KEY", "default-to-this-right-here")
    DATABASE_URL = os.getenv("DATABASE_URL")


class DevelopmentConfig(Config):
    """
    Enables the interactive debugger for use in development
    """
    DEBUG = True

class TestingConfig(Config):
    """
    Enables interactive debugger and propagates Exception
    for testing
    """
    DEBUG = True
    TESTING = True

class ProductionConfig(Config):
    """
    Disables interactive debugger and testing for use in
    Production server
    """
    DEBUG = False
    TESTING = False


app_config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig
}

