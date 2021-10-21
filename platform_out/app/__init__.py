from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import sys
from flask import jsonify
import logging
from elasticapm.contrib.flask import ElasticAPM

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

if os.getenv("SENTRY_DSN"):
    sentry_sdk.init(
        dsn=os.getenv("SENTRY_DSN"),
        integrations=[FlaskIntegration()]
    )

db = SQLAlchemy()
elastic_apm = ElasticAPM()


def create_app(script_info=None):

    # instantiate the app
    app = Flask(__name__)

    # set config
    app_settings = os.getenv("APP_SETTINGS")
    app.config.from_object(app_settings)

    logging.basicConfig(level=app.config["LOG_LEVEL"])

    # set up extensions
    db.init_app(app)
    elastic_apm.init_app(app)

    # register blueprints
    with app.app_context():
        from app.resources.observations import observations_blueprint

    app.register_blueprint(observations_blueprint)

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {"app": app, "db": db}

    @app.route("/")
    def hello_world():
        return jsonify(health="ok")

    @app.route("/debug-sentry")
    def trigger_error():
        division_by_zero = 1 / 0

    return app
