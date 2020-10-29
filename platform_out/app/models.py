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
    def filter_by_resultime(cls, minresulttime, maxresulttime):

        obs_list = []

        if not minresulttime:
            obs_list = Observations.query.filter(Observations.resulttime <= maxresulttime)

        elif not maxresulttime:
            obs_list = Observations.query.filter(Observations.resulttime >= minresulttime)

        else:
            obs_list = Observations.query.filter(
                and_(
                    Observations.resulttime <= maxresulttime,
                    Observations.resulttime >= minresulttime,
                )
            )

        def to_json(x):
            return {"result": x.result, "result time": x.resulttime}

        return {"Observations": list(map(lambda x: to_json(x), obs_list))}

    @classmethod
    def filter_by_thing_timebound(cls, thing, minresulttime, maxresulttime, minphenombegintime, maxphenombegintime):

        obs_list = (
            Observations.query.join(
                Datastreams, Observations.datastream_id == Datastreams.id
            )
            .add_columns(
                Observations.result,
                Observations.resulttime,
                Observations.phenomenontime_begin,
                Datastreams.id,
                Datastreams.thing_link,
                Datastreams.sensor_link,
            )
            .filter(
                and_(
                    Datastreams.thing_link == thing,
                    Observations.resulttime <= maxresulttime,
                    Observations.resulttime >= minresulttime,
                    Observations.phenomenontime_begin <= maxphenombegintime,
                    Observations.phenomenontime_begin >= minphenombegintime
                )
            )
        )

        def to_json(x):
            return {
                "result": x.result if x.result else "null",
                "result time": x.resulttime if x.resulttime else "null",
                "phenomenon time": x.phenomenontime_begin if x.phenomenontime_begin else "null",
                "datastream_id": x.id,
                "thing": x.thing_link,
                "sensor": x.sensor_link,
            }

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
