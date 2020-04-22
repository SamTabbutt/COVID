#LocationDict:
#
#
#Objects: 
#   locationDict:
#       locationDict makes a dictionary of the known data of each county in the united states organized by state
#       it is a composite dataFrame of the valuable census data pulled from (the internet--where?)
#
#Members:
#   df:
#       df is the composite pandas dataframe of all counties in the united states
#       Index: '<county name\{' County',' Parish',' Borough'}>, <state name>'
#       Example for indexing 'King County, Washington':
#           df.loc['King, Washington']
#   dict:
#       dict is a dictionary of all counties in the United States organized by state
#       Index: 'state name'
#       Example for subset of df for all counties in 'Washington' state:
#           dict['Washington']
#
#Fields:
#    **INDEX** : 'county, state':
#       description-- unique county, state combination of county of interest
#       format-- '<county_name\{'County','Parish','Borough'}>, <state_name>'
#       type-- String
#   'State':
#       description-- the US Sate of the county of interest
#       format-- 'state name'
#       type-- String
#   'Latitudue':
#       description-- central latitude of the county of interest
#       format-- degree of latitude
#       source-- geopy
#       type-- float64
#   'Logitude':
#       description-- central longitude of the county of interest
#       format-- degree of longitude taken from geopy
#       source-- geopy
#       type-- float64
#   'Population':
#       description-- total population of the county of interest
#       format-- taken from 2010 census data
#       source-- US Census
#       type-- int64
#   'Population Density':
#       description-- total population density of the county of interest
#       format-- total population/total land area of county
#       source-- US Census
#       type-- float64
#   'Land area':
#       description-- total land area of the county of interest
#       format-- square miles
#       source-- US Census
#       type-- float64
#   'SIP Order Date':
#       description-- the date of shelter in place order for the state of the county of interest
#       expceptions-- **If no shelter in place order for given state: df.loc['county, state','SIP Order Date'] = '0/0/0'**
#       format-- m/dd/yyyy
#       source-- https://www.finra.org/rules-guidance/key-topics/covid-19/shelter-in-place
#       type-- string by default
#
#   
#If fitData == True: each county will have associated logistic fit data and exponential fit data merged from 'counties/fitData.csv' including fields:
#   'logist params': parameters of the fit function y=c/(1+a*(exp)^(b(x-d)))+e in string representation of the numpy array [a b c d e]
#   'logist max error': the mean covarience of the logistic fit parameters
#   'exp params': parameters of the fit function y=a*(exp)^(bx)+c in string representation of the numpy array [a b c]
#   'exp max error': the mean covarience of the exponential fit parameters
#   'first case': the date of the first recorded case of COVID-19
#
#Calling for data in locationDict examples:
#   QUERY: Population density of King County, Washington:
#       ld = locationDict().dict
#       Washington_counties = ld['Washington']
#       King_County_Pop_Density = Washington_counties.loc['King, Washington','Population Density']
#       -------------------------------------OR---------------------------------------------------
#       ldf = locationDict().df
#       King_County_Pop_Density = ldf.loc['King, Washington', 'Population Density']
#   QUERY: Total population of Washington:
#       ld = locationDict().dict
#       Washington_population = ld['Washington']['Population'].sum()
#   QUERY: Total population density of Washington:
#       ld = locationDict().dict
#       Washington_population_density = ld['Washington']['Population'].sum()/ld['Washington']['Land area'].sum()
#   QUERY: Parameter 'a' of the logistical fit for King County, WA:
#       ld = locationDict(fitData=True).dict
#       Washington_counties = ld['Washington']
#       logistic_fit_params = np.fromstring(Washington_counties.loc['King, Washington','logist params'][1:-1],sep=' ')
#       a = logistic_fit_params[0]



import pandas as pd
import numpy as np
import os
from glob import glob

working_dir = os.path.dirname(os.path.realpath(__file__))
county_folder = os.path.join(working_dir,'PreprocessedCountyData')
geopy_locs_path = os.path.join(county_folder,'CountyLocationData.csv')
census_data_path = os.path.join(county_folder,'census.csv')

#create dict class to initialize a dict to call on location data
class locationDict:
    def __init__(self,useAll=True,keys=[]):
        self.useAll = useAll
        self.df = self.makeCompositeDf()
        self.dict =  self.makeDict(self.df)

    def makeCompositeDf(self):
        #Build stateDict to call on for specific location data
        #Create dataframe from coordinate and census data respectively        

        #Merge the dataframes by index
        if self.useAll:
            preprocessed_data_frames = []
            for countyData in glob(county_folder+'/*'):
                preprocessed_data_frames.append(pd.read_csv(countyData.set_index('county, state')))
            fullcounty_df = pd.concat(preprocessed_data_frames,axis=1,join='inner')
        else:
            preprocessed_data_frames = []
            for countyData in glob(county_folder+'/*'):
                if countyData.split('/')[-1] in keys:
                    preprocessed_data_frames.append(pd.read_csv(countyData.set_index('county, state')))
            fullcounty_df = pd.concat(preprocessed_data_frames,axis=1,join='inner')
        return fullcounty_df
    
    def makeDict(self,frame):
        #Group the full dataframe by state
        fullcounty_state_group = frame.groupby('State')
        #Create dict to call on the data from a state
        stateDict = {st[0]:st[1] for st in fullcounty_state_group}
        return stateDict
