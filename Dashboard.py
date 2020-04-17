#Main Logistical Fit tab of Bokeh Dashboard
#Extracts location and fit data through LocationDict
#Extracts case data from NYT COVID-19 dataset

import pandas as pd
import os
import math
from LocationDict import locationDict as ld
import numpy as np
from scipy import stats as scistats
from bokeh.plotting import figure, curdoc
from bokeh.io import show, output_notebook
import bokeh.models as bm
from bokeh.layouts import column,row

#Define local location data object to pull fit, census, and shelter in place data
locObject = ld(fitData=True)
locDict = locObject.dict
locDf = locObject.df
print(locDf.columns)

#Define local directory and create COVID dataframe in pandas
working_dir = os.path.dirname(os.path.realpath(__file__))
covid_dir = os.path.join(working_dir,'covid-19-data')
us_counties_path = os.path.join(covid_dir,'us-counties.csv')
covid_data = pd.read_csv(us_counties_path)
covid_data['county, state'] = covid_data['county']+', '+covid_data['state']
covid_data = covid_data.set_index('date')

#makeHist:
#      Input: 
#             dataFrame and variable of the dataFrame to generate histogram
#             r: range of data to inspect
#      Output:
#             Bokeh histogram plot of the series of the dataframe specified within the range specified
def makeHist(dataFrame,var,r):
       hist, edges = np.histogram(dataFrame[var], 
                            bins = 100,
                            range = [r[0],r[1]])

       delays = pd.DataFrame({var: hist, 
                       'left': edges[:-1], 
                       'right': edges[1:]})

       p = figure(plot_height = 120, plot_width = 400, 
              y_axis_label = 'Number of Counties')

       src = bm.ColumnDataSource(delays)
       p.quad(source=src,bottom=0, top=var, 
              left='left', right='right', 
              fill_color='red', line_color='black', hover_fill_color = 'navy')

       h = bm.HoverTool(tooltips = [(var+' value left', '@left'),
                            ('Number of counties', '@'+var)])

       p.add_tools(h)
       return p

#makeLowErrorDf:
#      Input: paramString: the string of the fit type to be analyzed
#      Normalization: the function normalizes the value for fit parameter c to a percentage of population infected
#      Output: a subset of locDf with expanded parameters as a column for each fit parameter and all fits with covarience<inf
def makeLowErrorDf(paramString):
       params_df = pd.DataFrame()
       params_df['params'] = locDf[paramString+' params'].apply(lambda x:np.fromstring(x[1:-1],sep=' '))
       params_df['Population'] = locDf['Population']
       params_df['error'] = locDf[paramString+' max error']
       highErrorInd = params_df[params_df['error']<10^5].index
       lowErrorDf = params_df.drop(highErrorInd)
       paramList = []
       for p in range(len(lowErrorDf['params'][0])):
              paramList.append(str(p))
       lowErrorDf[paramList] = pd.DataFrame(lowErrorDf.params.values.tolist(), index= lowErrorDf.index)
       lowErrorDf['2'] = lowErrorDf['2'].apply(lambda x:10000*x/lowErrorDf['Population'])
       lowErrorDf = lowErrorDf.drop('params',axis=1)
       return lowErrorDf, paramList

#makeParamsHistograms:
#      Input: 
#             paramString: the string of fit parameter to investigate
#             rangeMatrix: a list of ranges specifying the range of interest for each parameter of the model, respectively
#      Output:
#             A list of histogram plots in Bokeh format to be placed into a dashboard
def makeParamsHistograms(paramString,rangeMatrix):
       lowErrorDf,paramList = makeLowErrorDf(paramString)
       histList = []
       for i,p in enumerate(paramList):
              histList.append(makeHist(lowErrorDf,p,rangeMatrix[i]))

       return histList

#Make a list of histogram plots for both the logistic fit and exponential fit
#      -----For current iteration of dashboard, the exponential fit is not used------
loghists = makeParamsHistograms('logist',[[-5,40],[-1,.5],[0,2],[0,40],[-20,20]])
exphists = makeParamsHistograms('exp',[[0,10],[0,.5],[0,20]])

#getCountyData:
#      Input: name: the name of the county of interest in '<county_nam\{'County','Parish','Bureau'}>, <state_name>'
#Output:
#      Subset of NYT COVID data restricted to the county, state combination 
def getCountyData(name):
       county_data = covid_data[covid_data['county, state']==name]
       return county_data

#makeLogCurve:
#      Input: 
#             fit: list of logistic fit parameters [a,b,c,d,e] for logistic fit model y=c/(1+a*e^b(x-d))+e
#             length: length of array to plot
#      Output:
#             (x,y) values for curve y=c/(1+a*e^b(x-d))+e over length with (delta)x=1
def makeLogCurve(fit,length):
       a = fit[0]
       b = fit[1]
       c = fit[2]
       d = fit[3]
       e = fit[4]
       x_ = np.linspace(1,length,num=length)
       xmd = np.subtract(x_,np.full((length,),d))
       ex = xmd*b
       exp = a*np.exp(ex)
       denom = np.add(exp,np.full((len(exp),),1))
       y = np.add(np.true_divide(c,denom),np.full((len(exp),),e))
       x = np.linspace(1,length,num=length)
       return (x,y)

#getCountyTrend:
#      input: 
#             name: the name of the county of interest in '<county_nam\{'County','Parish','Bureau'}>, <state_name>'
#             length: the length of the model to create
#      output:
#             (x,y) values for curve y=c/(1+a*e^b(x-d))+e over length with (delta)x=1 from the parameters from fitData.csv
def getCountyTrend(name,length):
       x = locDf.loc[name,'logist params']
       print(locDf.loc[name,'logist max error'])
       fit = np.fromstring(x[1:-1],sep=' ')
       return makeLogCurve(fit,length)

#getParamString:
#      Input:
#             ar: fit parameter array for [a,b,c,d,e]
#             error: the max covarience of the fit data
#             first: the date of the first case
#      Output:
#             human readable string presenting the fit parameters, error, and first date of case
def getParamsString(ar,error,first):
       return 'Logistical fit paramters:\na: '+str(ar[0])+'\nb: '+str(ar[1])+'\nc: '+str(ar[2])+'\nd: '+str(ar[3])+'\ne: '+str(ar[4])+'\nmax covarience: '+str(1/error)+'\nfirst case: '+str(first)



#Initalize the dashboard with King County, Washington
data = getCountyData('King, Washington')
params = locDf.loc['King, Washington']['logist params']
parsed_p = np.fromstring(params[1:-1],sep=' ')
error = locDf.loc['King, Washington']['logist max error']
first = locDf.loc['King, Washington']['first case']
x = np.linspace(1,len(data),num=len(data))
y = data['cases']

#Define source, and s to be the display for the individual county of interest, displaying the NYT COVID-19 data and the logistical fit curve
source = bm.ColumnDataSource(data=dict(x=x,y=y))
s = figure(plot_width=400, plot_height=400,x_axis_label='Days since first case',y_axis_label='Number of cases')
s.line('x','y', source=source,line_width=2)

xt,yt = getCountyTrend('King, Washington', len(data))
source2 = bm.ColumnDataSource(data=dict(x=xt,y=yt))
s.line('x','y',source=source2,line_width=1,color='green')

#Present the fit parameters for the county of interest
stats = bm.PreText(text=getParamsString(parsed_p,error,first), width=50)

#Display the average logistical fit curve over all parameters [a,b,c,d,e]
lowErrorDf,paramList = makeLowErrorDf('logist')
paramMeans = []
for i in paramList:
       paramMeans.append(lowErrorDf[i].mean())
xm,ym = makeLogCurve(paramMeans,20)
meanSource = bm.ColumnDataSource(data=dict(x=xm,y=ym))
meanPlot = figure(width=400,height=200)
meanPlot.line('x','y',source=meanSource,line_width=2)

#Create selectors for selecting a state and county to view the data and model fit for
state_select = bm.Select(title='State',value='Washington',options=list(covid_data['state'].unique()))
county_select = bm.Select(title='County',value='King',options=list(covid_data[covid_data['state']=='Washington']['county'].unique()))

#Define update_counties to update county list based on the selected state
def update_counties(attr,old,new):
       selected_state = state_select.value
       county_select.options = list(covid_data[covid_data['state']==selected_state]['county'].unique())

state_select.on_change('value',update_counties)

#Define update plots to update the display of the interest county plot when the county_select is changed
def update_plots(attr,old,new):
       selected_state = state_select.value
       selected_county = county_select.value
       county_state = selected_county+', '+selected_state
       data = getCountyData(county_state)

       x = np.linspace(1,len(data),num=len(data))
       y = data['cases']
       source.data = dict(x=x,y=y)

       xt,yt = getCountyTrend(county_state, len(data))
       source2.data = dict(x=xt,y=yt)

       params = locDf.loc[county_state]['logist params']
       parsed_p = np.fromstring(params[1:-1],sep=' ')
       error = locDf.loc[county_state]['logist max error']
       first = locDf.loc[county_state]['first case']
       stats.text = getParamsString(parsed_p,error, first)

county_select.on_change('value',update_plots)

#Organize and display
ops = column(state_select,county_select,stats)
p = column(loghists)
layout = row(p,column(s,meanPlot),ops)

curdoc().add_root(layout)
