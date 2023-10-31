# Import the dependencies.
from flask import Flask, jsonify
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


#################################################
# Database Setup
#################################################

# reflect an existing database into a new model
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with= engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

app = Flask(__name__)

#getting lastest date and date of one year before that
def one_year_back():
    session = Session(bind=engine)
    session.query(measurement.date).order_by(measurement.date.desc()).first()
    
    #getting start date for one year range
    end_date = dt.datetime(2017,8,23) - dt.timedelta(days = 365)

    #close session
    session.close()

    return(end_date)

#################################################
# Flask Setup
#################################################
@app.route("/")
def home(): # need to figure out the proper text and cite it
    return """The routes that are available:
    <ul>
     <li>/api/v1.0/precipitation for Precipitation infomation in JSON format</li>
     <li>/api/v1.0/stations for a list of Stations in JSON format</li>
     <li>/api/v1.0/tobs for Temperature Observations (TOBS infomration in JSON format</li>
     <li>/api/v1.0/start for getting the minimum, average,and maximum temperature for a specified start date,
     where start in the link is replaced with YYYY-MM-DD
     </li>
     <li>/api/v1.0/start/end for getting the minimum, average,and maximum temperature for a specified start-end date range,
     where start and end in the link is replaced with YYYY-MM-DD </li>"""

@app.route("/api/v1.0/precipitation")
def precipitaion():
    # Create our session (link) from Python to the DB
    session = Session(bind=engine)

    #query data for precipitation for 1 year
    a_year_data = session.query(measurement.date, measurement.prcp).filter(measurement.date >= one_year_back()).all()
    
    #close session
    session.close()

    #saving query to dictionary and append to a list in prcp_data
    prcp_data = []
    for date, prcp in a_year_data:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = [prcp]
        prcp_data.append(prcp_dict)


    # return the dictionary in json format
    return jsonify(prcp_data)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(bind=engine)

    stations = session.query(station.station).all()
    
    #close session
    session.close()
    
    # Convert list of tuples into normal list
    all_stations = list(np.ravel(stations))

    #return the list of stations in json format
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(bind=engine)

    #query the selection, filtering by dates from a year from the lastest date where the station has the id of the most active station
    sel = [measurement.date, measurement.tobs]
    
    station_temp = session.query(*sel).\
    filter(measurement.date >= one_year_back(), measurement.station == 'USC00519281').all()
    
    #close session
    session.close()

    #saving query to dictionary and append to a list in tobs_date
    tobs_data = []
    for date, prcp in station_temp:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["prcp"] = [prcp]
        tobs_data.append(tobs_dict)
    #return the list of stations in json format
    return jsonify(tobs_data)

@app.route("/api/v1.0/<start>") # giving null output
def start_date(start):
    # Create our session (link) from Python to the DB
    session = Session(bind=engine)

    #https://www.programiz.com/python-programming/datetime
    start_date= dt.datetime.strptime(start, '%Y-%m-%d')

    sel = [func.min(measurement.tobs),
       func.max(measurement.tobs),
       func.avg(measurement.tobs)]

    data_from_start = session.query(*sel).\
        filter(measurement.date >= start_date).all()
    
    #close session
    session.close()

    from_start = list(np.ravel(data_from_start))

    #return the min, max, and average in json format
    return jsonify(from_start)

@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    # Create our session (link) from Python to the DB
    session = Session(bind=engine)

    start_date= dt.datetime.strptime(start, '%Y-%m-%d')
    end_date= dt.datetime.strptime(end,'%Y-%m-%d')

    sel = [func.min(measurement.tobs),
       func.max(measurement.tobs),
       func.avg(measurement.tobs)]

    data_from_start_end = session.query(*sel).\
        filter(measurement.date >= start_date).filter(measurement.date <= end_date).all()
    
    #close session
    session.close()
    
    from_start_end = list(np.ravel(data_from_start_end))

    #return the min, max, and average in json format
    return jsonify(from_start_end)
#################################################
# Flask Routes
#################################################
if __name__ == '__main__':
    app.run(debug=True)