#CensusData.py:
#Description: parses 2010 US Census Data and assigns population and area data to the common domain
#Objects: CensusData:
#   child of DataModule
#Data Input: 'DataSoures/census.csv'

import pandas as pd
import numpy as np
import os
from .PreprocessingModule import DataModule

#Child of DataModule to parse population, housing, and area data of the common domain
class CensusData(DataModule):
    def processData(self,df_init):
        #Define data source path
        current_dir = os.path.dirname(os.path.realpath(__file__))
        working_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
        source_folder = os.path.join(working_dir,'DataSources')
        census_data_path = os.path.join(source_folder,'census.csv')

        #Read .csv file with specific encoding
        census_df = pd.read_csv(census_data_path, encoding = "ISO-8859-1")
        #Drop all rows that do not have 'County', 'Parish', 'City', or 'Borough'
        census_df = census_df[census_df['Geographic area.1'].str.contains("County") | census_df['Geographic area.1'].str.contains("Parish")| census_df['Geographic area.1'].str.contains("City")| census_df['Geographic area.1'].str.contains("Borough")]
        census_df.index = df_init.index
        #Drop columns without intrinsic properties
        census_df = census_df.drop(['Id','Id2','Target Geo Id','Target Geo Id2'],axis=1)
        #Rename columns for easy calling and reading
        new_cols = []
        for col in census_df.columns:
            if 'Area' in col:
                newName = col.split(' - ')[1]
                new_cols.append(newName)
            elif 'Density' in col:
                newName = col.split(' - ')[1]+' Density'
                new_cols.append(newName)
            else:
                new_cols.append(col)
        census_df.columns = new_cols

        #Create 'State' column
        census_df['State'] = df_init.index
        census_df['State'] = census_df['State'].apply(lambda x:x.split(', ')[1])
        #Remove strings from population column and set type to float
        census_df['Population'] = census_df['Population'].apply(lambda x:x.split('(')[0]).astype('float64')
        #Drop unnecesarry columns
        census_df = census_df.drop('Geographic area.1', axis=1)
        census_df = census_df.drop('Geographic area',axis=1)
        census_df = census_df.drop('Geography',axis=1)

        return census_df

    def setMetaInfo(self):
        moduleClassName = 'CensusData'
        source = 'US 2010 Census'
        domain = 'CensusCounties'
        author = 'United States Census Bureau'
        return {'moduleName':moduleClassName,'source':source,'domain':domain,'author':author}
