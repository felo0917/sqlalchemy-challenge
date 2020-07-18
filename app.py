import numpy as np
import datetime as dt

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
hawaii_measurement = Base.classes.measurement
hawaii_station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
#################################################

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"Precipitation: /api/v1.0/precipitation<br/>"
        f"List of Stations: /api/v1.0/stations<br/>"
        f"Temperature observations for last year: /api/v1.0/tobs<br/>"
        f"Temperature statistics from the start date(2016-08-23): /api/v1.0/<start>"
        f"Temperature statistics from start to end dates(2017-08-23): /api/v1.0/<start>/<end>"
    )


@app.route('/api/v1.0/precipitation')
def precipitation():
    session = Session(engine)
    table = [hawaii_measurement.date, hawaii_measurement.prcp]
    results = session.query(*table).all()
    session.close()

    precipitation = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["Date"] = date
        prcp_dict["Precipitation"] = prcp
        precipitation.append(prcp_dict)

    return jsonify(precipitation)

@app.route('/api/v1.0/stations')
def stations():
    session = Session(engine)
    table = [hawaii_station.station,hawaii_station.name]
    results = session.query(*table).all()
    session.close()

    stations = []
    for station,name in results:
        station_dict = {}
        station_dict["Station"] = station
        station_dict["Name"] = name
        stations.append(station_dict)

    return jsonify(stations)


@app.route('/api/v1.0/tobs')
def tobs():
    session = Session(engine)
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    table = [hawaii_measurement.date,hawaii_measurement.tobs]
    results = session.query(*table).filter(hawaii_measurement.date >= year_ago).all()
    session.close()

    tobsall = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict["Date"] = date
        tobs_dict["Tobs"] = tobs
        tobsall.append(tobs_dict)

    return jsonify(tobsall)


@app.route('/api/v1.0/<start>')
def start(start):
    session = Session(engine)
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(func.min(hawaii_measurement.tobs), func.avg(hawaii_measurement.tobs), func.max(hawaii_measurement.tobs)).\
        filter(hawaii_measurement.date >= year_ago).all()
    session.close()

    tobsstart = []
    for min,avg,max in results:
        tobs_dict = {}
        tobs_dict["Min"] = min
        tobs_dict["Average"] = avg
        tobs_dict["Max"] = max
        tobsstart.append(tobs_dict)

    return jsonify(tobsstart)


@app.route('/api/v1.0/<start>/<stop>')
def start_stop(start,stop):
    session = Session(engine)
    year_ago = dt.date(2015, 8, 23) - dt.timedelta(days=365)
    stop = dt.date(2015, 8, 23)
    results = session.query(func.min(hawaii_measurement.tobs), func.avg(hawaii_measurement.tobs), func.max(hawaii_measurement.tobs)).\
        filter(hawaii_measurement.date >= year_ago).filter(hawaii_measurement.date <= stop).all()
    session.close()

    tobsstart_stop = []
    for min,avg,max in results:
        tobs_dict = {}
        tobs_dict["Min"] = min
        tobs_dict["Average"] = avg
        tobs_dict["Max"] = max
        tobsstart_stop.append(tobs_dict)

    return jsonify(tobsstart_stop)

if __name__ == '__main__':
    app.run(debug=True)