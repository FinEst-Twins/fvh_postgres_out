from flask import jsonify, request, Blueprint, current_app
from flask_restful import Resource, Api
from datetime import datetime
import json
import os
from app.models import Observations, Datastreams
from datetime import datetime
import logging
from flask_sqlalchemy import SQLAlchemy

logging.basicConfig(level=logging.INFO)


observations_blueprint = Blueprint("observations", __name__)
api = Api(observations_blueprint)


class Observation(Resource):
    def get(self):
        """
        gets list of all observations
        """
        try:
            query_parameters = request.args
            obs_list = []
            if query_parameters:

                min_resulttime = None
                max_resulttime = None
                thing = None

                if 'minresulttime' in query_parameters:
                    min_resulttime = request.args['minresulttime']
                    min_resulttime = datetime.strptime(min_resulttime, '%Y-%m-%d,%H:%M:%S.%f')

                if 'maxresulttime' in query_parameters:
                    max_resulttime = request.args['maxresulttime']
                    max_resulttime = datetime.strptime(max_resulttime, '%Y-%m-%d,%H:%M:%S.%f')

                if "thing" in query_parameters:
                    thing = request.args["thing"]

                if thing and min_resulttime and max_resulttime:
                    obs_list = Observations.filter_by_thing_timebound(thing, min_resulttime, max_resulttime)

                else:
                    result = {"message":"query parameters thing, minresultime and maxresulttime expected"}
                    response = jsonify(result)
                    response.status_code = 400
                    return response

        except Exception as e:
            logging.error(e)
            result = {"message": "error"}
            response = jsonify(result)
            response.status_code = 400
            return response


        if obs_list:

            response = jsonify(obs_list)
            response.status_code = 200
            return response
        else:
            result = {"message": "No observations found"}
            response = jsonify(result)
            response.status_code = 200
            return response


api.add_resource(Observation, "/observation")


