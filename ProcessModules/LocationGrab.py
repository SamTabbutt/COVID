#LocationGrab:
#Data Input: GeoPy nominatim location data
#Assigns a latitude and langitude to each unique county

import pandas as pd
import numpy as np
from geopy.geocoders import Nominatim
import os
from .PreprocessingModule import DataModule

#Child of DataModule to interpret geographic location of the common domain
class GeoData(DataModule):
    def processData(self,df_init):
        #do_geocode:
        #Input: location string
        #If the geocode database recognizes the the county in <county>, <state> format: return geocode object
        #Else: return a geocode object of <state>
        def do_geocode(county,count):
            locator = Nominatim(user_agent="myGeocoder")
            if count == 0:
                print("Locator timing out.. Might want to try again later")
                return 0
            try:
                return locator.geocode(county,featuretype='county')
            except:
                count-=1
                return do_geocode(county.split(', ')[0],count)

        #getCoord:
        #Input: location string
        #If the geocode object has valid latitude and longitude fields: return '<latitude>, <longitude>'
        #Else: return '0, 0'
        def getCoord(county):
            #location = do_geocode(county,7)
            try:
                '''print(county,'found.','Lat:',location.latitude,'Long:',location.longitude)
                return str(location.latitude)+', '+str(location.longitude)'''
                return '0, 0'
            except:
                print(county, "not found")
                return '0, 0'

        #Use common domain as index
        uniqueCounty = pd.DataFrame()
        uniqueCounty['county, state'] = df_init.index
        #Apply getCoord to each 'county, state' combination in the common domain.
        uniqueCounty['County Lat/long'] = uniqueCounty['county, state'].apply(getCoord)
        #Split latitude and longitude
        uniqueCounty['Latitude'] = uniqueCounty['County Lat/long'].apply(lambda x:x.split(', ')[0])
        uniqueCounty['Longitude'] = uniqueCounty['County Lat/long'].apply(lambda x:x.split(', ')[1])
        uniqueCounty = uniqueCounty.drop('County Lat/long', axis=1)
        uniqueCounty = uniqueCounty.set_index('county, state')
        #Ship dataframe
        return uniqueCounty

    def setMetaInfo(self):
        outputFileName = 'countyCoordinates'
        moduleClassName = 'GeoData'
        source = 'geopy nominatim'
        domain = 'CensusCounties'
        author = 'Geopy data'
        return {'outputFileName':outputFileName,'moduleClassName':moduleClassName,'source':source,'domain':domain,'author':author}