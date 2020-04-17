#LocationGrab:
#Input: NYT COVID-19 us-counties csv
#Assigns a latitude and langitude to each unique county
#Output: dataframe csv with location lat/long data

import pandas as pd
import numpy as np
from geopy.geocoders import Nominatim
import os

#Define the path directories to the .csv files of interest
current_dir = os.path.dirname(os.path.realpath(__file__))
working_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
data_dir = os.path.join(working_dir,'covid-19-data')
county_path = os.path.join(data_dir,'us-counties.csv')

#Create pandas dataframe of NYT COVID-19 county data
df = pd.read_csv(county_path)

#do_geocode:
#Input: location string
#If the geocode database recognizes the the county in <county>, <state> format: return geocode object
#Else: return a geocode object of <state>
def do_geocode(county):
    locator = Nominatim(user_agent="myGeocoder")
    try:
        return locator.geocode(county,featuretype='county')
    except:
        return do_geocode(county.split(', ')[0])

#getCoord:
#Input: location string
#If the geocode object has valid latitude and longitude fields: return '<latitude>, <longitude>'
#Else: return '0, 0'
def getCoord(county):
    location = do_geocode(county)
    try:
        print(county,location.latitude)
        return str(location.latitude)+', '+str(location.longitude)
    except:
        print(county, "not found")
        return '0, 0'

#Create DataFrame of unique 'county, state' objects
#   There are many repeated county names throughout the country
def getLatLongFrame():
    uniqueCounty = pd.DataFrame()
    df['county, state'] = df['county']+' County, '+df['state']
    uniqueCounty['county, state'] = df['county, state'].unique()
    uniqueCounty['County Lat/long'] = uniqueCounty['county, state'].apply(getCoord)
    return uniqueCounty