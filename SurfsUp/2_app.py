# Import the dependencies.
from flask import Flask, jsonify
import datetime as dt
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base

app = Flask(__name__)

#################################################
# Database Setup
#################################################

engine = create_engine('sqlite:///Resources/hawaii.sqlite', connect_args={'check_same_thread': False}, echo=True)

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
Session = sessionmaker(bind=engine)
session = Session()


#################################################
# Flask Setup
#################################################
@app.route("/")
def home():
    print("Server received request for Home page")
    return (
        f"Welcome to our Climate Analysis home page!<br/>"
        f"&nbsp;<br/>"
        f"Available Routes:<br/>"
        f"&nbsp;&nbsp;/api/v1.0/precipitation<br/>"
        f"&nbsp;&nbsp;/api/v1.0/stations<br/>"
        f"&nbsp;&nbsp;/api/v1.0/tobs<br/>"
        f"&nbsp;&nbsp;/api/v1.0/StartDate<br/>"
        f"&nbsp;&nbsp;/api/v1.0/StartDate/EndDate<br/>"
        f"&nbsp;<br/>"
        f"Note: Use StartDate and EndDate in yyyy-mm-dd format<br/>"
        f"&nbsp;&nbsp;Example: <i>/api/v1.0/2016-08-24/2017-08-23</i>"
    )

# Precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Calculate the date one year ago from the most recent date
    most_recent_date = session.query(func.max(measurement.date)).scalar()
    one_year_ago = dt.datetime.strptime(most_recent_date, '%Y-%m-%d') - dt.timedelta(days=365)
    
    # Query precipitation data for the last 12 months
    precip_data = session.query(measurement.date, measurement.prcp).filter(measurement.date >= one_year_ago).all()
    
    # Create a dictionary with date as the key and prcp as the value
    precip_dict = {date: prcp for date, prcp in precip_data}
    
    return jsonify(precip_dict)

# Stations route
@app.route("/api/v1.0/stations")
def stations():
    # Query and list of stations
    station_results = session.query(station.station).all()
    stations_list = [station[0] for station in station_results]
    
    return jsonify(stations_list)

# Temperature observations route
@app.route("/api/v1.0/tobs")
def tobs():
    # Get the most active station ID
    most_active_station = session.query(measurement.station).group_by(measurement.station).order_by(func.count(measurement.station).desc()).first()[0]
    
    # Calculate the date one year ago from the most recent date
    most_recent_date = session.query(func.max(measurement.date)).filter(measurement.station == most_active_station).scalar()
    one_year_ago = dt.datetime.strptime(most_recent_date, '%Y-%m-%d') - dt.timedelta(days=365)
    
    # Query temperature observations for the last 12 months for the most active station
    temp_data = session.query(measurement.date, measurement.tobs).filter(measurement.station == most_active_station).filter(measurement.date >= one_year_ago).all()
     # Convert Row objects to dictionaries
    temp_list = [{"date": row.date, "tobs": row.tobs} for row in temp_data]
    
    return jsonify(temp_list)

# Temperature statistics route
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def temp_stats(start, end=None):
    if not end:
        end = session.query(func.max(measurement.date)).scalar()
    
    # Query temperature statistics for the specified date range
    temp_stats = session.query(func.min(measurement.tobs),
                        func.avg(measurement.tobs),
                        func.max(measurement.tobs)).filter(measurement.date >= start).filter(measurement.date <= end).all()
    
    # Unpack the results
    min_temp, avg_temp, max_temp = temp_stats[0]
    
    return jsonify({"start_date": start, "end_date": end, "TMIN": min_temp, "TAVG": avg_temp, "TMAX": max_temp})

if __name__ == "__main__":
    app.run(debug=True)