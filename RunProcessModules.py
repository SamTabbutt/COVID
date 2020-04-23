#RunProcessModules.py:
#Discription: The file is run to occupy the data files in the folder 'PreprocessedCountyData/'
#   It loops through selected data processing modules and extracts the resulting dataframe.
#   If the dataframe meets the data format requirements, the data is saved as a .csv and updates the metaData.csv file
#By default, RunProcessModules.py will run each module in 'FullModuleClassList'
#If desired to run select modules, use command line interface:
#   - command parameters:
#       - [1] - 'include' or 'exclude'
#           - if [1] == 'include', then:
#               - [2] - 'all' - runs each process module provided in fullModuleClassList
#               - [2],[3],[4],... - name of each DataModule child to run separated by ' '
#           - if [1] == 'exclude', then:
#               - [2],[3],[4],... - name of each DataModule to exclude from running sequence separated by ' '
#       - EXAMPLES
#           - To run modules 'ShelterData' and 'CensusData':
#               python RunProcessModules.py include ShelterData CensusData
#           - To run all modules excluing 'GeoData':
#`              python RunProcessModules.py exclude GeoData
#           - To run all modules:
#               python RunProcessModules.py include all
#
#UPDATES PROCEDURE NOTE:
#   In the addition of a process module, update the list:
#       fullModuleClassList+= <data_module_class_name>

#Command and server imports
import sys
import os
#Data manipulation imports
import pandas as pd
import numpy as np
#Data modules import
import ProcessModules
#Datetime import
from datetime import datetime

#Create full list 
fullModuleClassList = ['ShelterData','GeoData','CensusData','LogisticalFit']

#buildModuleClassList:
#   Input: command list from the system
#   initiate empty moduleClassList to run and fill with commands
#   Output: full list of class names to run from ProcessModules
def buildModuleClassList(commandList):
    moduleClassList = []
    if commandList[1] == 'include':
        for i,moduleName in enumerate(commandList):
            if i<2:
                continue
            if commandList[2] == 'all':
                moduleClassList = fullModuleClassList
                break
            moduleClassList.append(moduleName)

    elif commandList[1] == 'exclude':
        moduleClassList = fullModuleClassList
        for i,moduleName in enumerate(commandList):
            if i<2:
                continue
            try:
                moduleClassList.remove(moduleName)
            except:
                print(moduleName+' not found')

    else:
        moduleClassList = fullModuleClassList
    
    return moduleClassList

#Run buildModuleClassList with command line parameter list
moduleClassList = buildModuleClassList(sys.argv)

#Define working_dir
working_dir = os.path.dirname(os.path.realpath(__file__))
#Define data output directory
data_output_dir = os.path.join(working_dir,'PreprocessedCountyData')

#saveCSV:
#Input:
#   - dataModule: an instance of a child of DataModule
#   - fileName: the output filename of the data
#Saves dataframe defined in dataModule in 'data_output_dir/<fileName>.csv'
#Output: none

def saveCSV(dataModule,fileName):
    df = dataModule.df
    df.to_csv(os.path.join(data_output_dir,fileName+'.csv'))

#Define location of metaData.csv
metaDataLocation = os.path.join(data_output_dir,'metaData.csv')
#Define global metaDf from metaDataLocation
global metaDf
metaDf = pd.read_csv(metaDataLocation)

#updateMeta:
#Input:
#   - metaDf: the current metaDf dataframe
#   - metaInfo: the metaData information for a single row of metaData
#Adds a row into metaDf containing the metaData for a single datasource
#Output: updated metaDf with row summarizing new data, including the datetime of update for that row.
def updateMeta(metaDf,metaInfo):
    metaInfo.update({'last updated':datetime.now()})
    dropIndex = metaDf[metaDf['moduleName']==metaInfo['moduleName']].index
    metaDf = metaDf.drop(dropIndex)
    newRow = pd.DataFrame(metaInfo,index =['TEMP'])
    metaDf = pd.concat([metaDf,newRow])
    return metaDf


#verifyFormat:
#Input:
#   - dataModuleInst: an instance of a data module
#Output:
#   - Boolean: true if the dataModuleInst meets required data format. False if it does not
def verifyFormat(dataModuleInst):
    formatModule = ProcessModules.PreprocessingModule.DataModule()
    formatDf = formatModule.df_init
    sampleDf = dataModuleInst.df
    if formatDf.index == sampleDf.index:
        return True
    else:
        return False


#Loop through each module in ProcessModules
for string in ProcessModules.__dict__:
    #if the module name is in moduleClassList, and the module is callable, create instance of data module
    dataModule = ProcessModules.__dict__[string]
    if string in moduleClassList:
        if callable(dataModule):
            processedData = dataModule()
            if verifyFormat(processedData):
                #Get metaData info for the module
                metaInfo = processedData.getMetaInfo()
                #Save dataframe from the module
                saveCSV(processedData,string)
                #Update metaData
                metaDf = updateMeta(metaDf,metaInfo)
            else:
                print(string,'not formatted correctly')
        else:
            print(string+' not valid object')

#Save updated metaData
metaDf.to_csv(metaDataLocation,index=False)