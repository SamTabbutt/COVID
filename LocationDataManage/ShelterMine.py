#ShelterMine:
#Input: URL https://www.finra.org/rules-guidance/key-topics/covid-19/shelter-in-place
#Data mine of the data presented by finra on the date of shelter in place orders by state
#Output: dataframe of each unique 'county, state' combination in NYT COVID-19 data and its associated date of shelter in place order
#   If the state has not implimented shelter in place, the date will read '0/0/0'
import pandas as pd
from bs4 import BeautifulSoup
import requests
import os

#Define directories
current_dir = os.path.dirname(os.path.realpath(__file__))
working_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
covid_dir = os.path.join(working_dir,'covid-19-data')
county_path = os.path.join(covid_dir,'us-counties.csv')

#Create pandas dataframe of NYT COVID-19 county data
df = pd.read_csv(county_path)

def getShelterFrame():
    #Request HTTP from input url and parse as HTML
    r = requests.get('https://www.finra.org/rules-guidance/key-topics/covid-19/shelter-in-place')
    soup = BeautifulSoup(r.text, 'html.parser')

    #Parse through the table which presents shelter in place data
    table = soup.find(lambda tag: tag.name=='table')
    rows = table.findAll(lambda tag: tag.name=='tr')
    #Define dictionary to return the string of the date for the input of a state name
    entries = {}
    for i,r in enumerate(rows):
        if i==0:
            continue
        entry = r.findAll('td')
        print(entry[0].getText(),entry[3].getText())
        entries.update({entry[0].getText():entry[3].getText()})

    #Assign a shelter in place date to each unique 'county, state' combination in the NYT COVID-19 us-counties csv
    sipList = []
    uniqueCounty = pd.DataFrame()
    df['county, state'] = df['county']+' County, '+df['state']
    uniqueCounty['county, state'] = df['county, state'].unique()
    for row in uniqueCounty.index:
        statename = uniqueCounty.iloc[row]['county, state'].split(', ')[1]
        try:
            sipList.append(entries[statename])
        except:
            sipList.append('0/0/0')

    uniqueCounty['SIP Order Date'] = sipList
    return uniqueCounty