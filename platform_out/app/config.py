import os
import logging

basedir = os.path.abspath(os.path.dirname(__file__))


def get_env_variable(name):
    try:
        return os.environ[name]
    except KeyError:
        message = "Expected environment variable '{}' not set.".format(name)
        logging.error(message)
        raise Exception(message)


class Config(object):

    SECRET_KEY = os.environ.get("SECRET_KEY")
    DEBUG = True
    CSRF_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True

    ELASTIC_APM = {
        "SERVICE_NAME": get_env_variable("ELASTIC_SERVICE_NAME"),
        "SECRET_TOKEN": get_env_variable("ELASTIC_SECRET_TOKEN"),
        "SERVER_URL": get_env_variable("ELASTIC_SERVER_URL"),
        "DEBUG": True,
    }


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SECRET_KEY = os.environ.get("SECRET_KEY")


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    TESTING = False
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_ECHO = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_TEST_URL")
    SECRET_KEY = os.environ.get("SECRET_KEY")
