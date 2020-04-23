#PreprocessingModule:
#Houses the parent class for any module which fits data into the common domain
#
#Objects:
#   - DataModule:
#       Discr:
#           - DataModule is the format for any file parsing raw data into the common format for locationDict.
#           - All modules which intend to accomplish this must use DataModule as a parent, altering necesarry classes
#       Fields:
#           - df_init: DataFrame with index set as the common domain: '<county_name>, <state_name>'.
#               - there are no columns set in df_init
#           - df: the DataFrame containing proper data organized on the domain of df_init
#   `       - metaInfo: a dictionary of the required metaData information for the collective project
#       Permanent Methods:
#           - setIndex():
#               - sets the domain for the dataframe as the common domain: '<county_name>, <state_name>'
#           - getDfInfo():
#               - retreives information of the dataframe after it has been defined, including:
#                   - number of fields
#                   - names of field for each field
#                   - type of field for each field
#               - these are passed as a dictionary along with the data-input by the author
#       Mutable Methods:
#           - processData(self,df_init):
#               Input: df_init
#               Output: updated DataFrame created based on the common domain defined and implimented to df_init
#               Note: under circumstances where a similar domain is defined, be sure to merge any new data with df_init, maintaining the domain of df_init
#           -  setMetaInfo(self):
#               Input: None
#               Output: Dictionary of valuable metaData from the author
#   `           Note: the Dictionary must maintain each field indicated. If the author does not have a response to the field, ze must fill 'N/A', or leave blank
# `
#PROCEDURE NOTE:
#   When implimenting a new module which inherits any preprocessing module, be sure to update:
#       1) the file ProcessModules.__init__.py with the import of the new module
#       2) the file RunProcessModules.py with the name of the object in the list 'FullModuleClassList'
# 


import pandas as pd
import numpy as np
import os

class DataModule():
    def __init__(self):
        self.df_init = self.setIndex()
        self.df = self.processData(self.df_init)
        self.metaInfo = self.setMetaInfo()
        self.metaInfo.update(self.getDfInfo(self.df))

    #MUTIBLE:
    #df_init input to be used as index for all additional information
    def processData(self,df_init):
        return df_init

    #MUTIBLE:
    #Author-entered information about the data and desired outputFileName
    def setMetaInfo(self):
        moduleClassName = ''
        source = ''
        domain = 'CensusCounties'
        author = ''
        return {'moduleName':moduleClassName,'source':source,'domain':domain,'author':author}

    #PERMANENT
    #Parses the US Census 2010 data and extracts a list of each unique county, state combination.
    #Defines an initial DataFrame with this list as the index
    #Returns initial DataFrame
    def setIndex(self):
        #Define path to census data .csv file
        current_dir = os.path.dirname(os.path.realpath(__file__))
        working_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
        source_folder = os.path.join(working_dir,'DataSources')
        census_data_path = os.path.join(source_folder,'census.csv')

        #Open census data as a DataFrame
        census_df = pd.read_csv(census_data_path, encoding = "ISO-8859-1")
        df_init = pd.DataFrame()
        #Define state parsing function
        def grabState(entry):
            try:
                stateName = entry.split(' - ')[1]
            except:
                stateName = entry.split(' - ')[0]
            return stateName

        #Define function to remove the tag from the county, presenting as the name of the county, parish, borough, city, etc.
        def removeTag(entry):
            if 'County' in entry:
                entry = entry.replace(' County','')
            if 'Parish' in entry:
                entry = entry.replace(' Parish','')
            if 'Borough' in entry:
                entry = entry.replace(' Borough','')
            return entry
        
        #Pull state name from geographic area column
        census_df['State'] = census_df['Geographic area'].apply(grabState)
        #Reduce data to only have county information. 
        census_df = census_df[census_df['Geographic area.1'].str.contains("County") | census_df['Geographic area.1'].str.contains("Parish")| census_df['Geographic area.1'].str.contains("City")| census_df['Geographic area.1'].str.contains("Borough")]
        #Remove all 'County', 'Parish', etc phrases
        census_df['Geographic area.1'] = census_df['Geographic area.1'].apply(removeTag)

        #Create 'county, state' column for index to match with coordinate dataframe
        df_init['county, state'] = census_df['Geographic area.1'] +', ' +census_df['State']

        df_init = df_init.set_index('county, state')
        return df_init

    #PERMANENT FUNCTION
    #Returns the: (1) number of fields, (2) list of name of each field, (3) list of type of each field
    def getDfInfo(self,df):
        column_count = len(df.columns)
        columns = [c for c in df.columns]
        types = [str(t) for t in df.dtypes]
        return {'field count':column_count,'field names':str(columns),'field types':str(types)}

    #PERMANENT FUNCTION
    #Returns the metaInfo of the data as a dictionary
    def getMetaInfo(self):
        return self.metaInfo