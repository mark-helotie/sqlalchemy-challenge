# Import the dependencies
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)


#################################################
# Flask Setup
#################################################

app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return (
        f"Welcome to my Climate Analysis'Home' page!"
        f"/api/v1.0/precipitation<br>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/<start><br>"
        f"/api/v1.0/<start>/<end><br>"
    )

# Precipitation date over the last year (12months)
@app.route("/api/v1.0/precipitation")
def precipitation():
    year_ago = dt.date(2017, 8,23) - dt.timedelta(days=365)
    dataframe_a = (session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > year_ago).order_by(Measurement.date).all())
    dataframe_b = pd.DataFrame(dataframe_a, columns=["Date", "Precipitation"])
    dataframe_b = dataframe_b.sort_values("Date").set_index("Date")
   
    dictionary_A = dict(dataframe_b) 
     # returns json list of dictionary   
    return jsonify(dictionary_A)


# Return a JSON list of stations
@app.route("/api/v1.0/stations")
def stations():
    stations = session.query(Station.name, Station.station).all()

    dictionary_B = dict(stations)  
     # returns json list of dictionary  
    return jsonify(dictionary_B)


# Most active station for the previous year
@app.route("/api/v1.0/tobs")
def act_stat():

    active_station = session.query(Measurement.station,func.count(Measurement.station)).\
        .group_by(Measurement.station).\
        .order_by(func.count(Measurement.station).\
        .desc()).all()
    
    dictionary_c = dict(active_station)

    # returns json list of dictionary
    return jsonify(dictionary_c)


@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def date(start, end):

if start:
session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
    .filter(Measurement.date >= start).all()

if end:
session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
    .filter(Measurement.date <= end).all()

if __name__ == "__main__":
    app.run(debug=True)
