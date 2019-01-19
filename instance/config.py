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
    DEBUG = False
    TESTING = True
    DATABASE_URL = os.getenv("DATABASE_TEST_URL")


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
