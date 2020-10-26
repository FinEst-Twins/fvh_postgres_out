from app import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
from sqlalchemy.dialects.postgresql import HSTORE, JSON
from sqlalchemy.ext.mutable import MutableDict
import logging
import json
from sqlalchemy.ext import mutable

logging.basicConfig(level=logging.INFO)


class Observations(db.Model):
    __tablename__ = "observation"
    id = db.Column(db.Integer, primary_key=True)
    phenomenontime_begin = db.Column(db.DateTime(), index=True)
    phenomenontime_end = db.Column(db.DateTime(), index=True)
    resulttime = db.Column(db.DateTime(), index=True)
    result = db.Column(db.String(), index=True)
    resultquality = db.Column(db.String(), index=True)
    validtime_begin = db.Column(db.DateTime(), index=True)
    validtime_end = db.Column(db.DateTime(), index=True)
    resultquality = db.Column(db.String(), index=True)
    # parameters = db.Column(JsonEncodedDict)
    # parameters = db.Column(MutableDict.as_mutable(JSON))
    datastream_id = db.Column(db.Integer, index=True)
    featureofintrest_link = db.Column(db.String(), index=True)

    def __repr__(self):
        return f"<Observation {self.result}, {self.resulttime}>"

    @classmethod
    def filter_by_resultime(cls, mintime, maxtime):

        obs_list = []

        if not mintime:
            obs_list = Observations.query.filter(Observations.resulttime <= maxtime)

        elif not maxtime:
            obs_list = Observations.query.filter(Observations.resulttime >= mintime)

        else:
            obs_list = Observations.query.filter(
                and_(
                    Observations.resulttime <= maxtime,
                    Observations.resulttime >= mintime,
                )
            )

        def to_json(x):
            return {"result": x.result, "result time": x.resulttime}

        return {"Observations": list(map(lambda x: to_json(x), obs_list))}


    @classmethod
    def filter_by_thing_timebound(cls, thing, mintime, maxtime):

        obs_list = Observations.query.join(Datastreams, Observations.datastream_id == Datastreams.id)\
                        .add_columns(Observations.result, Observations.resulttime, Datastreams.id, Datastreams.thing_link, Datastreams.sensor_link)\
                            .filter(and_(Datastreams.thing_link == thing,Observations.resulttime <= maxtime,Observations.resulttime >= mintime))

        def to_json(x):
            return {"result": x.result, "result time": x.resulttime, "datastream_id" : x.id, "thing" : x.thing_link, "sensor" : x.sensor_link}

        return {"Observations": list(map(lambda x: to_json(x), obs_list))}


class Datastreams(db.Model):
    __tablename__ = "datastream"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    description = db.Column(db.String())
    observedarea = db.Column(db.String())
    unitofmeasurement = db.Column(db.String())
    observationtype = db.Column(db.String())
    phenomenontime_begin = db.Column(db.DateTime())
    phenomenontime_end = db.Column(db.DateTime())
    resulttime_begin = db.Column(db.DateTime())
    resulttime_end = db.Column(db.DateTime())
    sensor_link = db.Column(db.String())
    thing_link = db.Column(db.String())
    observedproperty_link = db.Column(db.String())

    def __repr__(self):
        return f"<Observation {self.name}, {self.description}>"

    @classmethod
    def filter_by_thing_sensor(cls, thing, sensor):

        datastream_list = []
        if (not thing) and sensor:
            datastream_list = Datastreams.query.filter(
                Datastreams.sensor_link == sensor
            )

        elif (not sensor) and thing:
            datastream_list = Datastreams.query.filter(Datastreams.thing_link == thing)

        else:
            datastream_list = Datastreams.query.filter(
                and_(
                    Datastreams.thing_link == thing,
                    Datastreams.sensor_link == sensor,
                )
            )

        def to_json(x):
            return {"datastream_id": x.id, "name": x.name, "description": x.description}

        return {"Datastreams": list(map(lambda x: to_json(x), datastream_list))}
