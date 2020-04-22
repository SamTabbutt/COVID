import pandas as pd
import numpy as np
import os

class DataModule():
    def __init__(self):
        self.df_init = self.setIndex()
        self.df = self.processData(self.df_init)
        self.metaInfo = self.setMetaInfo()
        self.metaInfo.update(self.getDfInfo(self.df))

    def processData(self,df_init):
        return df_init

    def setMetaInfo(self):
        outputFileName = ''
        moduleClassName = ''
        source = ''
        domain = 'CensusCounties'
        author = ''
        return {'outputFileName':outputFileName,'moduleClassName':moduleClassName,'source':source,'domain':domain,'author':author}

    def setIndex(self):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        working_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
        source_folder = os.path.join(working_dir,'DataSources')
        census_data_path = os.path.join(source_folder,'census.csv')

        census_df = pd.read_csv(census_data_path, encoding = "ISO-8859-1")
        df_init = pd.DataFrame()
        def grabState(entry):
            try:
                stateName = entry.split(' - ')[1]
            except:
                stateName = entry.split(' - ')[0]
            return stateName

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
        census_df = census_df[census_df['Geographic area.1'].str.contains("County") | census_df['Geographic area.1'].str.contains("Parish")| census_df['Geographic area.1'].str.contains("City")]
        #Remove all 'County', 'Parish', etc phrases
        census_df['Geographic area.1'] = census_df['Geographic area.1'].apply(removeTag)

        #Create 'county, state' column for index to match with coordinate dataframe
        df_init['county, state'] = census_df['Geographic area.1'] +', ' +census_df['State']

        df_init = df_init.set_index('county, state')
        return df_init

    def getDfInfo(self,df):
        column_count = len(df.columns)
        columns = [c for c in df.columns]
        types = [str(t) for t in df.dtypes]
        return {'field count':column_count,'field names':str(columns),'field types':str(types)}

    def getMetaInfo(self):
        return self.metaInfo