#LocationDict:
#Description: LocationDict creates a dataframe with the common domain and a selected group of data in the folder 'PreprocessedCountyData/'
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
#Creating an instance of locationDict:
#   By default, the dataframe will be a collection of all the data in 'PreprocessedCountyData/'
#   To create an instance of locationDict with select data sources:
#       set useAll=False
#       set include = ['<data_module[0]>','<data_module[1]>',...,'<data_module[n]>']
#
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
    def __init__(self,useAll=True,include=[]):
        self.useAll = useAll
        self.df = self.makeCompositeDf()
        self.dict =  self.makeDict(self.df)

    def makeCompositeDf(self):      
        #Merge the dataframes by index (common domain)
        if self.useAll:
            preprocessed_data_frames = []
            for countyDataPath in glob(county_folder+'/*'):
                if 'metaData' in countyDataPath:
                    continue
                preprocessed_data_frames.append(pd.read_csv(countyDataPath.set_index('county, state')))
            fullcounty_df = pd.concat(preprocessed_data_frames,axis=1,join='inner')
        else:
            preprocessed_data_frames = []
            for countyDataPath in glob(county_folder+'/*'):
                if countyDataPath.split('/')[-1].split('.csv')[0] in keys:
                    preprocessed_data_frames.append(pd.read_csv(countyData.set_index('county, state')))
            fullcounty_df = pd.concat(preprocessed_data_frames,axis=1,join='inner')
        return fullcounty_df
    
    def makeDict(self,frame):
        #Group the full dataframe by state
        fullcounty_state_group = frame.groupby('State')
        #Create dict to call on the data from a state
        stateDict = {st[0]:st[1] for st in fullcounty_state_group}
        return stateDict
