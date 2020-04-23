# COVID
This project combines data from various sources in attempt to provide accessible routes of analysis of COVID-19 based on location-specific data. 

There are two main sources of high-dimentional data available through this project. The first is the raw data cloned from the [New York Times COVID-19 database](https://github.com/nytimes/covid-19-data), including case and death data from each county in the United States. This data is available through a .csv file. The second is a dynamic Pandas dataFrame as a conglomerate of data. The format of the project allows for any extention of data as it applied to United States county-specific data.

## Project Structure:

The project is structured to house any county-specific data as it might be of interest to analysis of variables of the COVID-19 pandemic. In its current iteration, the preprocessed data consists of:
- 2010 US Census Data
- Geographic coordinate data
- Shelter in place order dates data
- Logistical and Exponential fits of coronavirus cases

The project is structured to house Processing modules which parse data and fit data to a **common domain** of 'county, state'.
- The phrase **common domain** is used frequently throughout this project, and refers to the set of unique 'county, state' combinations available in the 2010 US Census Dataset. In a mathematical sense, it is the domain of any function with the range of values as the resulting column.

The modules are called through the python file ```RunProcessModules```.

Once the data is preprocessed and stored, it is accessible via ```LocationDict.py```, through the object ```locationDict``` the data can be easily mutated, analyzed, and visualized. 

The project currently contains ```LogisticDash.py``` which is an example dashboard of how data can be demonstrated through ```locationDict``` and the data source ```DataSources/covid-19-data/us-counties.csv```

### Data Pipeline
![text](https://github.com/SamTabbutt/COVID/blob/master/Misc/Display/Generalized.jpg)
- Process 1: Data is located from a source
- Process 2: Data is formatted into a **common domain** using the ```PreprocessingModule.py``` format
- Process 3: The unique data module is run by ```RunProcessingModule.py``` and returns a data frame
- Process 4: The dataframe is passed through a format verification gate and, if properly formatted, the meta data for that set is recorded in ```LocationDataManage/metaData.csv```, and the preprocessed data is saved as a unique .csv file in ```LocationDataManage/```
- Process 5: The data is called by ```LocationDict.py``` and mutible to visualize and analyze. 

#### Running the preprocessing modules:
RunProcessModules.py:

Discription: The file is run to populate and update the data files in the folder ```'PreprocessedCountyData/'``` as well as update ```PreprocessedCountyData/metaData.csv```

Command line interface:
- command parameters:
  - [1] - 'include' or 'exclude'
    - if [1] == 'include', then:
      - [2] == 'all' : runs each process module provided in fullModuleClassList
      - [2],[3],[4],... - name of each DataModule child to run separated by ' '
    - if [1] == 'exclude', then:
      - [2],[3],[4],... - name of each DataModule to exclude from running sequence separated by ' '
- EXAMPLES
  - To run modules 'ShelterData' and 'CensusData':
      ```python RunProcessModules.py include ShelterData CensusData```
  - To run all modules excluing 'GeoData':
      ```python RunProcessModules.py exclude GeoData```
  - To run all modules:
      ```python RunProcessModules.py include all```

#### Adding a preprocessing module:
To contribute data to the set of preprocessed data, one must create a preprocessing module and save it in the ```ProcessModules/``` file path.

A preprocessing module has two strict requirements:
- It must contain a field ```self.df``` which is a pandas dataframe with the index as the **common domain**, which is a list of each unique county, state combination in the 2010 US census database. 
- It must contain a method ```getMetaInfo(self)``` which returns a dictionary of metaData regarding the data module, including:
  - ```'moduleClassName'```: the name of the object
  - ```'Source'```: the source of the data in the module
  - ```'Domain'```: In the current iteration of the pipeline, each module must have the domain ```'CensusCounties'```
  - ```'Author'```: The author of the module/data source
  - ```'field count'```: The number of data fields in the dataset
  - ```'field names'```: A list of the name of each field in the data set
  - ```'field types'```: A list of the datatype of each field in the data set

For ease of use,  ```PreprocessingDataModule.py``` has been created as the parent to any preprocessing data module, in which the only necesarry updates are:
- Update the method ```processData(seld,df_init)```. The dataframe ```df_init``` is passed as a dataframe solely consisting of an index which is the **common domain**. The method must return a dataframe maintaining the index of ```df_init```.
- Update the method ```setMetaInfo(self)``` to house the correct metadata info intrinsic to the dataset.

Once a new module has been created and saved in the ```ProcessModules/``` path, the module must be added to the file ```ProcessModules/__init__.py```, and the list of object names: ```fullModuleClassList``` must be updated with the name of the new module. 


### LocationDict
The location dictionary is the main resource for inquiries regarding location specific variables of the COVID data collected and distributed through the New York Times. locationDict is the primary object in LocationDict.py. It merges data of each county in the United States into one data frame which can be called directly, or can be used to easily return subsets of the data frame based on a specific state of interest. 

#### Preparing the dictionary:

Once the preprocessing modules have been run and populated the folder ```PreprocessedCountyData/``` with the respective .csv files, ```LocationDict.py``` is capable of easily combining and dropping necesarry data columns from the pool of collected and preprocessed data. 

The ```metaData.csv``` file is a good resource to understand what data is available to be accessed by locationDict, as all updated .csv files will be recorded in the ```metaData.csv``` file.

#### Using locationDict class:

By default, creating an instance of ```locationDict``` will include the all data in ```PreprocessedCountyData/```

To create an instance of ```locationDict``` which does not include all data in ```PreprocessedCountyData/```:
- set parameter ```useAll = False```
- set parameter ```include = ['<data_module[0]>','<data_module[1]>',...,'<data_module[n]>']```
- EXAMPLE:
    ```locDict = locationDict(useAll=False,include=['CensusData','LogisticalFit'])```

Once an instance of ```locationDict``` has been created, there are two fields for data manipulation, visualization, and analysis:
- df:
  - df is the composite pandas dataframe of all counties in the united states
  - Index: **common domain**
  - Example for indexing 'King County, Washington':
 
        df.loc['King, Washington']
 
- dict:
  - dict is a dictionary of all counties in the United States organized by state     
  - Index: ```'state name'```    
  - Example for subset of df for all counties in 'Washington' state:
       
        dict['Washington']

**Columns:**
The columns of the dataframe will be the columns from the chosen preprocessed datasets. By default, this will be every column listed in the ```metaData.csv ``` file. If an instance of locationDict is created of a subset of the available preprocessed datasets, then the columns will be restricted to the columns of the chosen datasets.

**Examples:**
- QUERY: Population density of King County, Washington:
   
       locDict = locationDict()
       ld = locDict.dict
       Washington_counties = ld['Washington']
       King_County_Pop_Density = Washington_counties.loc['King, Washington','Population Density']
OR
       
       locDict = locationDict()
       ldf = locDict.df
       King_County_Pop_Density = ldf.loc['King, Washington', 'Population Density']
       
- QUERY: Total population of Washington:

       locDict = locationDict()
       ld = locDict.dict
       Washington_population = ld['Washington']['Population'].sum()

- QUERY: Total population density of Washington:

       locDict = locationDict()
       ld = locDict.dict
       Washington_population_density = ld['Washington']['Population'].sum()/ld['Washington']['Land area'].sum()

- QUERY: Parameter 'a' of the logistical fit for King County, WA:

       locDict = locationDict(fitData=True)
       ld = locDict.dict
       Washington_counties = ld['Washington']
       logistic_fit_params = np.fromstring(Washington_counties.loc['King, Washington','logist params'][1:-1],sep=' ')
       a = logistic_fit_params[0]

## Constructing Dashboards

locationDict is a dynamic pandas dataframe easily adapted to present location-specific data for the COVID crisis. 


### An example dashboard displaying results from loogisticalFit.py:
![text](https://github.com/SamTabbutt/COVID/blob/master/Misc/Display/Ex.gif)


The data collected from the NYT COVID-19 data set combined with the data from locationDict create dynamic opportunities for exploring variables of the trends of the virus.

In this example of a dashboard, the logistical fit data which has a mean covariance less than 10^5 was discarded for the distribution display. An issue which is currently being sorted is the parameter C, which is dependent on the population size of the county of interest. The data should be normalized as a percentage of population exposed rather than a total case number representation. In addition, a lot of the fits seem to not be the best fit for a logistical curve. For example, King County, Washington is obviously a logistical trend, however the method of fit did not find the true best fit for the data. 

There are thousands of interesting ways to visualize and analyze this data for a better public understanding of the trends of the virus. Moving forward, I will be working on developing more easily-interpreted visualizations as well as various statistical analysis of location-variable effects on the growth-rate and inflection point of the logistical curves. 

Thanks for reading, and if you have any thoughts, suggestions, or questions feel free to reach out at samtabbutt@gmail.com.


