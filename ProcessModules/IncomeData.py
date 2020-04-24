#IncomeData.py:
#Description: parses 2010 US Census Data and assigns population and area data to the common domain
#Objects: CensusData:
#   child of DataModule
#Source: https://www.bea.gov/data/income-saving/personal-income-county-metro-and-other-areas
#Data Input: 'DataSoures/WealthDist.csv'

import pandas as pd
import numpy as np
import os
from .PreprocessingModule import DataModule

class IncomeData(DataModule):
    def processData(self,df_init):
        #Define data source path
        current_dir = os.path.dirname(os.path.realpath(__file__)) 
        working_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
        source_folder = os.path.join(working_dir,'DataSources')
        income_data_path = os.path.join(source_folder,'WealthDist.csv')

        #make dataframe from WealthDist.csv
        incomeDf = pd.read_csv(income_data_path)
        #Initiate loop boolean as need for new state
        reset_state = False
        #Initiate statname and iteration count
        stateName = ''
        i = 0
        #Fillna with empty string
        incomeDf = incomeDf.fillna('')
        while i<max(incomeDf.index):
            #Follow each empty row with a new set to the state name
            if reset_state == True:
                stateName = incomeDf.loc[i]['location']
                incomeDf = incomeDf.drop(i)
                reset_state = False
                i+=1
            elif incomeDf.loc[i]['location']=='':
                reset_state = True
                incomeDf = incomeDf.drop(i)
                i+=1
            #Update each county name to fit standard format with previous state name
            else:
                incomeDf.loc[i]['location'] = incomeDf.loc[i]['location']+', '+stateName
                i+=1

        #Convert numerical columns to floats
        stringObjs = incomeDf.columns[incomeDf.dtypes=='object']
        for col in stringObjs:
            if col == 'location':
                continue
            else:
                incomeDf[col] = incomeDf[col].apply(lambda x:str(x))
                incomeDf[col]=incomeDf[col].apply(lambda x:x.replace(',',''))
                incomeDf[col] = incomeDf[col].replace('',0)
                incomeDf[col] = incomeDf[col].astype('float64')
        #Rename and index the domain
        incomeDf['county, state'] = incomeDf['location']
        incomeDf = incomeDf.drop('location',axis=1)
        incomeDf = incomeDf.set_index('county, state')
        #Drop 'Richmond, Virginia' because it was created twice
        incomeDf = incomeDf.drop('Richmond, Virginia')
        #Reindex to common domain and return frame
        df = pd.concat([df_init, incomeDf.reindex(df_init.index)], axis=1)
        return df


    def setMetaInfo(self):
        moduleClassName = 'IncomeData'
        source = 'bea.gov'
        domain = 'CensusCounties'
        author = 'US Wealth Tracking'
        return {'moduleName':moduleClassName,'source':source,'domain':domain,'author':author}