import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all routes that are available."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Convert the query results to a Dictionary using `date` as the key and `prcp` as the value"""
    """Return the JSON representation of your dictionary"""
    
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all precipitations
    results = session.query(Measurement.date, Measurement.prcp).all()

    # Create a dictionary from the row data and append to a list of all_precipitations
    all_precipitations = []
    for precipitation in results:
        precipitation_dict = {}
        precipitation_dict[precipitation.date] = precipitation.prcp
        all_precipitations.append(precipitation_dict)

    return jsonify(all_precipitations)

@app.route("/api/v1.0/stations")
def stations():
    """Return a JSON list of stations from the dataset"""
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all stations
    results = session.query(Station.name).all()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)

@app.route("/api/v1.0/tobs")
def tobs():
    """query for the dates and temperature observations from a year from the last data point."""
    """Return a JSON list of Temperature Observations (tobs) for the previous year."""
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all temperatures
    results = session.query(Measurement.date, Measurement.tobs).all()

    # Create a dictionary from the row data and append to a list of all_temp
    all_temps = []
    for temperature in results:
        temp_dict = {}
        temp_dict[temperature.date] = temperature.tobs
        all_temps.append(temp_dict)

    return jsonify(all_temps)

@app.route("/api/v1.0/<start>")
def find_stats_start(start):
    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range."""
    """When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date."""
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all statios
    results = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).group_by(Measurement.date).all()

    # Create a dictionary from the row data and append to a list of all_stations
    all_temps = []
    for temp in results:
        temps_dict = {}
        temps_dict["date"] = temp[0]
        temps_dict["tmin"] = temp[1]
        temps_dict["tavg"] = temp[2]
        temps_dict["tmax"] = temp[3]
        all_temps.append(temps_dict)

    return jsonify(all_temps)

@app.route("/api/v1.0/<start>/<end>")
def find_stats_startend(start, end):
    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range."""
    """When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive."""
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all statios
    results = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).group_by(Measurement.date).all()

    # Create a dictionary from the row data and append to a list of all_stations
    all_temps = []
    for temp in results:
        temps_dict = {}
        temps_dict["date"] = temp[0]
        temps_dict["tmin"] = temp[1]
        temps_dict["tavg"] = temp[2]
        temps_dict["tmax"] = temp[3]
        all_temps.append(temps_dict)

    return jsonify(all_temps)

if __name__ == '__main__':
    app.run(debug=True)
