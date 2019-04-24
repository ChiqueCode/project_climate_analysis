# Dependancies
import datetime as dt
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# References to the tables
print(Base.classes.keys())
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

# Creating an app
app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/<start>/<end>"
    )

#  Convert the query results to a Dictionary using `date` as the key and `prcp` as the value.

#  Return the JSON representation of your dictionary.
@app.route("/api/v1.0/precipitation/")
def prcp():
    results = session.query(Measurement.date, Measurement.prcp) 

    all_prcp = []
    for key, value in results:
        prcp_dict = {}
        prcp_dict[key] = value
        all_prcp.append(prcp_dict)    
    return jsonify(all_prcp)  


# Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations/")
def station():
    results = session.query(Station.station) 
    stations = []
    for station in results:
        if station not in stations:
            stations.append(station)
        else:
            break
    return jsonify(stations)  

Query for the dates and temperature observations from a year from the last data point.
Return a JSON list of Temperature Observations (tobs) for the previous year.
@app.route("/api/v1.0/tobs")  
def tobs():
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= "2016-08-23").filter(Measurement.date <= "2017-08-23").all()
    tobs_dict = {date: temp for date, temp in results}
    return jsonify(tobs_dict)

#  When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.
@app.route("/api/v1.0/<start_date>")
def one_day(start_date):
    one_day = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()
    trip_one_day = list(np.ravel(one_day))
    return jsonify(trip_one_day)

#When given the start and the end date, calculate the #`TMIN`, `TAVG`, and `TMAX` for dates between the #start and end date inclusive.
@app.route("/api/v1.0/<start_date>/<end_date>")
def all_days(start_date, end_date):
    all_days = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    trip_all_days = list(np.ravel(all_days))
    return jsonify(trip_all_days)

if __name__ == '__main__':
    app.run(debug=True)