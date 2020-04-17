#SaveLocationData:
#Grabs lat/long dataframe and 'shelter in place ' dataframe
#Merges the dataframes and saves the merged dataframe as CountyLocationData.csv

from LocationGrab import getLatLongFrame as GrabGeo
from ShelterMine import getShelterFrame as GrabShelter
import pandas as pd
import os

geo = GrabGeo()
CountyLocationDataDF = geo.merge(GrabShelter())

current_dir = os.path.dirname(os.path.realpath(__file__))
working_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
county_dir = os.path.join(working_dir,'counties')

CountyLocationDataDF.to_csv(os.path.join(county_dir,'CountyLocationData.csv'))
