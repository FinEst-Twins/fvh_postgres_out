from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import sys
from flask import jsonify
import logging
from elasticapm.contrib.flask import ElasticAPM

logging.basicConfig(level=logging.INFO)

db = SQLAlchemy()
elastic_apm = ElasticAPM()


def create_app(script_info=None):

    # instantiate the app
    app = Flask(__name__)

    # set config
    app_settings = os.getenv("APP_SETTINGS")
    app.config.from_object(app_settings)

    # set up extensions
    db.init_app(app)
    elastic_apm.init_app(app)

    # register blueprints
    from app.resources.observations import observations_blueprint

    app.register_blueprint(observations_blueprint)

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {"app": app, "db": db}

    @app.route("/")
    def hello_world():
        return jsonify(health="ok")

    return app
