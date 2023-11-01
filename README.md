# sqlalchemy-challenge

## SurfsUp
This folder contains the Resource folder, which contains the hawaii.sqlite file, which holds the measurements and stations data. The resource folder also contains the hawaii_measurements.csv and hawaii_stations.csv files which hold the same data as the hawaii.sqlite file, but in csv form.

Aside from the Resource folder, the SurfsUp folder also contains a climate_starter.ipynb script as well as a Python app.py script.

The climate_starter.ipynb script analyzes the measurement data and the station data in the hawaii.sqlite file. The Jupyter Notebook script analyzes the precipitation data to create a plot of the amount of inches of rain recorded in the last year of the dataset, as well as calculate the summary statistics for the precipitation. The script analyzes the station data to create a histogram of the observed temperature from the most active station from the past year. 

The app.py script creates an api that has 5 routes other than home:
- a precipation route, which gives the precipitation measurement and the date of the mesurement of the last year of the dataset in JSON format
- a stations route, which gives a list of the stations that record the measurement in JSON format
- a tobs (temperature observation) route, which returns a list of temperature observations for the previous year in JSON format
- a start route, which returnas a list of the minimum temperature, average temperature, and maximum temperature for a specificed start date to the end of the data set
- a start/end route, which returnas a list of the minimum temperature, average temperature, and maximum temperature for a specificed start date to the specificed end date

## Citations
- the climate_starter.ipynb used code from the website: https://docs.sqlalchemy.org/en/20/core/functions.html to find the functions func.count(), func.min(), and func.max()
- the app.py used code from the website: #https://www.programiz.com/python-programming/datetime to convert an object into a date object
