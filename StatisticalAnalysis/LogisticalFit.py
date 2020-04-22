#LogisticalFit:
#Input: NYT COVID-19 case data by county
#Output: fitData.csv saved in <working_dir>/counties/ associating logistical fit and exponential fit data for each county in the original data set
#The fits are derived using LSM algorithms through scipy.optimize library

import pandas as pd
import numpy as np
import os
import math
from scipy.optimize import curve_fit 

#Define working directory and data source location
current_dir = os.path.dirname(os.path.realpath(__file__))
working_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
covid_dir = os.path.join(working_dir,'covid-19-data')
us_counties_path = os.path.join(covid_dir,'us-counties.csv')

#Open data and create unique 'county, state' column
covid_data = pd.read_csv(us_counties_path)
covid_data['county, state'] = covid_data['county']+', '+covid_data['state']
covid_data = covid_data.set_index('date')
#Group by unique 'county, state' values
covid_county_groupings = covid_data.groupby('county, state')

#Define exponential fit model function
def expFunc(x,a, b,c): 
    return a*np.exp(b*x)+c

#Define exponential fit function. If the model is unable to fit, return parameters [0,0,0] with inf covarience
def fitExp(county_df):
    day_count_df = county_df.reset_index()
    try:
        fit, param_cov = curve_fit(expFunc, day_count_df.index, day_count_df['cases']) 
    except:
        fit = [0,0,0]
        param_cov=[[0]]
    return fit,param_cov

#Define logistical fit model function
def logisticFunc(x,a,b,c,d,e):
    return c/(1+a*np.exp(b*(x-d)))+e

#Define logistical fit function. If the model is unable to fit, return parameters [0,0,0,0,0] with inf covarience
def fitLogistic(day_count_df):
    try:
        i = np.inf
        fit, param_cov = curve_fit(logisticFunc, day_count_df.index, day_count_df['cases'],p0=[1,-2,50,10,1],bounds=([-i,-i,0,-i,-i],[i,0,i,i,i])) 
    except:
        fit = np.array([0,0,0,0,0])
        param_cov=[[0]]
        print('Not fit')
    return fit,param_cov

#Loop through county groupings and run the exp and logist fit for each sequence of data
density_data = []
for i,county_data in enumerate(covid_county_groupings):
    print("Running "+county_data[0])
    day_count_df = county_data[1].reset_index()
    params,error = fitLogistic(day_count_df)
    e1 = np.array(error).mean()
    params2,error2 = fitExp(day_count_df)
    e2 = np.array(error2).mean()
    try:
        #Create running list of parameters and error values with each parameter array stored as one single value in the running array
        density_data.append([county_data[0],params,e1,params2,e2,county_data[1].index[0]])
    except:
        print('not found',state,county_data[0])

#Save parameter and error values associated with each county under <working_dir>/counties/fitData.csv
logData = pd.DataFrame(density_data,columns=['county, state','logist params','logist max error','exp params','exp max error','first case'])
logData = logData.set_index('county, state')
logData.to_csv(os.path.join(working_dir,'counties/fitData.csv'))