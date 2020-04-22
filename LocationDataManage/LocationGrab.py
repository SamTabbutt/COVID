#LocationGrab:
#Input: NYT COVID-19 us-counties csv
#Assigns a latitude and langitude to each unique county
#Output: dataframe csv with location lat/long data

import pandas as pd
import numpy as np
from geopy.geocoders import Nominatim
import os
from .PreprocessingModule import DataModule

class GeoData(DataModule):
    def processData(self,df_init):
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
            #location = do_geocode(county)
            try:
                '''print(county,'found.','Lat:',location.latitude,'Long:',location.longitude)
                return str(location.latitude)+', '+str(location.longitude)'''
                return '0, 0'
            except:
                print(county, "not found")
                return '0, 0'

        #Create DataFrame of unique 'county, state' objects
        #   There are many repeated county names throughout the country
        uniqueCounty = pd.DataFrame()
        uniqueCounty['county, state'] = df_init.index
        uniqueCounty['County Lat/long'] = uniqueCounty['county, state'].apply(getCoord)
        uniqueCounty['Latitude'] = uniqueCounty['County Lat/long'].apply(lambda x:x.split(', ')[0])
        uniqueCounty['Longitude'] = uniqueCounty['County Lat/long'].apply(lambda x:x.split(', ')[1])
        uniqueCounty = uniqueCounty.drop('County Lat/long', axis=1)
        uniqueCounty = uniqueCounty.set_index('county, state')
        return uniqueCounty

    def setMetaInfo(self):
        outputFileName = 'countyCoordinates'
        moduleClassName = 'GeoData'
        source = 'geopy nominatim'
        domain = 'CensusCounties'
        author = 'Geopy data'
        return {'outputFileName':outputFileName,'moduleClassName':moduleClassName,'source':source,'domain':domain,'author':author}