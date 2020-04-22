import sys
import os
import pandas as pd
import numpy as np
import LocationDataManage
from datetime import datetime

fullModuleClassList = ['ShelterData','GeoData','CensusData']

def buildModuleClassList():
    moduleClassList = []

    if sys.argv[1] == 'include':
        for i,moduleName in enumerate(sys.argv):
            if i<2:
                continue
            if sys.argv[2] == 'all':
                moduleClassList = fullModuleClassList
                break
            moduleClassList.append(moduleName)

    elif sys.argv[1] == 'exclude':
        moduleClassList = fullModuleClassList
        for i,moduleName in enumerate(sys.argv):
            if i<2:
                continue
            try:
                moduleClassList.remove(moduleName)
            except:
                print(moduleName+' not found')

    else:
        moduleClassList = fullModuleClassList
    
    return moduleClassList

moduleClassList = buildModuleClassList()

working_dir = os.path.dirname(os.path.realpath(__file__))
data_output_dir = os.path.join(working_dir,'PreprocessedCountyData')

def saveCSV(dataModule,fileName):
    df = dataModule.df
    df.to_csv(os.path.join(data_output_dir,fileName+'.csv'))

metaDataLocation = os.path.join(data_output_dir,'metaData.csv')
global metaDf
metaDf = pd.read_csv(metaDataLocation)
def updateMeta(metaDf,metaInfo):
    metaInfo.update({'last updated':datetime.now()})
    dropIndex = metaDf[metaDf['outputFileName']==metaInfo['outputFileName']].index
    metaDf = metaDf.drop(dropIndex)
    newRow = pd.DataFrame(metaInfo,index =['TEMP'])
    metaDf = pd.concat([metaDf,newRow])
    return metaDf


for string in LocationDataManage.__dict__:
    val = LocationDataManage.__dict__[string]
    if string in moduleClassList:
        processedData = val()
        metaInfo = processedData.getMetaInfo()
        csvFileName = metaInfo['outputFileName']
        saveCSV(processedData,csvFileName)
        metaDf = updateMeta(metaDf,metaInfo)

metaDf.to_csv(metaDataLocation,index=False)