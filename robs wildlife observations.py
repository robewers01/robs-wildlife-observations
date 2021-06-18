#And also changed in the branch

from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
#import geopandas as gpd
import os
#import matplotlib as plt
import pandas as pd
import pyepicollect as pyep



##Download data from www.five.epicollect.net and do basic clean
#Add info from private app
CLIENT_ID = 2391
CLIENT_SECRET = 'gSf50WmsKtkNpoJdiIZSlVc5yLFnzc3UU8HufNwu'
SLUG = 'robs-wildlife-observations'
token = pyep.auth.request_token(CLIENT_ID, CLIENT_SECRET)
entries = pyep.api.get_entries(SLUG, token['access_token'])
data = entries['data']['entries']
#Work through pagination on Epicollect
while entries['meta']['current_page'] < entries['meta']['last_page']:
    entries = pyep.api.get_entries(SLUG, token['access_token'], page=(entries['meta']['current_page']+1))
    data = data + entries['data']['entries']
#Convert to pandas dataframe
form = pd.DataFrame(data)
#Clean data
form['Date'] = pd.to_datetime(form['10_Date'])      #Convert dates to datetime format
formComplete = form[form['4_Taxa'].notnull()]       #Remove records with unknown taxa


##Summarise the total number of species and taxa identified in the dataset
def speciesSummary(formComplete) :
    '''Function to report on the total number of taxa identified within a dataset'''
    numUniqueSppTot = 0                     #Holder for number of unique species
    uniqueTaxa = formComplete['4_Taxa'].unique()
    #Report number of species per taxa
    for x in range(0, len(uniqueTaxa)):     #Iterate through each unique taxon
        formTaxa = formComplete[formComplete['4_Taxa'] == uniqueTaxa[x]]    #Subset the form to include just that taxon   
        species = formTaxa['2_Species']     #Extract column with all species records
        uniqueSpp = species.unique()        #Extract unique species
        numUniqueSpp = len(uniqueSpp)       #Count the number of unique species
        if uniqueTaxa[x] == 'Plant' or uniqueTaxa[x] == 'Invertebrate':    #Define if taxa are identified to family or species level
            idLevel = 'families'
            #Work out species and genus records for taxa with primary ID at family level
            binomials = pd.Series(formTaxa['8_Latin_binomial'].dropna().unique())    #Extract unique set of Latin recorded Latin binomial IDs
            morphospp = binomials.str.endswith(' sp')   #Which have been identified to morphospecies/genus vs species?
            numMorpho = len(binomials[morphospp])       #Number of genus/morphospecies IDs
            numSpp = len(binomials) - numMorpho         #Number of species-level IDs
            genera = binomials.str.split(expand = True)[0].unique() #List of unique genera
            numGenera = len(genera)
            numUniqueSppTot += len(binomials)           #Update count of unique species
            print('You have seen', numUniqueSpp, str(idLevel), 'of', uniqueTaxa[x], '\n   including at least', numGenera, 'genera and', numSpp, 'identified species')     #Print the output
        else:
            idLevel = 'species'
            numUniqueSppTot += numUniqueSpp           #Update count of unique species
            print('You have seen', numUniqueSpp, str(idLevel), 'of', uniqueTaxa[x])     #Print the output
        #Print the total number of taxa observed
    print('In total, you have identified', numUniqueSppTot, 'species or morphospecies')           

##Report on most recent day, week, month or year
def recentReport(formComplete, period) :
    '''Function to give a summary of observations seen within a day, week, month or year of today's date, or of the total dataset'''
    today = pd.to_datetime(date.today())    #Get today's date
    #Subset form according to time period wanted
    if period == 'day' :
        formRecent = formComplete[formComplete['Date'] == today]       #Subset today's data
        formOld = formComplete[formComplete['Date'] != today]           #Subset data from all other dates
        timeRef = 'Today'
    elif period == 'week' :
        earliest = today - timedelta(days = 7)
        formRecent = formComplete[formComplete['Date'] >= earliest]    #Subset this week's data
        formOld = formComplete[formComplete['Date'] < earliest]     #Subset data from all other dates
        timeRef = 'This week'
    elif period == 'month' :
        earliest = today - relativedelta(months = +1)
        formRecent = formComplete[formComplete['Date'] >= earliest]    #Subset this month's data
        formOld = formComplete[formComplete['Date'] < earliest]     #Subset data from all other dates
        timeRef = 'This month'
    elif period == 'year' :
        earliest = today - relativedelta(years = +1)
        formRecent = formComplete[formComplete['Date'] >= earliest]    #Subset this year's data
        formOld = formComplete[formComplete['Date'] < earliest]     #Subset data from all other dates
        timeRef = 'This year'
    elif period == 'total' :
        formRecent = formComplete
    
    if period == 'total' :
        print('In total:')
    else :
        print('In the last', period, ':')
    print(speciesSummary(formRecent))
    return formRecent






operation = input("What would you like to do?\n  Enter 1 for a summary of the taxa you've recorded\n")
if operation == '1' :
    duration = input("What timeframe are you interested in?\n  Enter 1 for day\n  Enter 2 for week\n  Enter 3 for month\n  Enter 4 for year\n Enter 5 for no time limit\n")
else :
    print('not an option')




operation = input("What would you like to do?\n  Enter 1 for a summary of the taxa you've recorded\n")
if operation == '1' :
    duration = input("What timeframe are you interested in?\n  Enter 1 for day\n  Enter 2 for week\n  Enter 3 for month\n  Enter 4 for year\n Enter 5 for no time limit\n")
else :
    print("That's not an option douchebag")




    if duration == '1':
        recentReport(formComplete, 'day')
    elif duration == '2':
        recentReport(formComplete, 'week')
    elif duration == '3':
        recentReport(formComplete, 'month')
    elif duration == '4':
        recentReport(formComplete, 'year')
    elif duration == '5':
        recentReport(formComplete, 'total')
    else:
        print("That's not one of the options I gave you")
else:
    print("That's not one of the options I gave you")



operation = input("What would you like to do?\n  Enter 1 for a summary of the taxa you've recorded\n")
if operation == '1' :
    duration = input("What timeframe are you interested in?\n  Enter 1 for day\n  Enter 2 for week\n  Enter 3 for month\n  Enter 4 for year\n Enter 5 for no time limit\n")
else :
    print("That's not an option douchebag")


#would you like to download the data?

#would you like more details - Yes/No?
    #would you like a list of species? Which taxa?
    #Rare species report?
    #Local area report?
#record day/week/month/year
    #including/excluding zoos

#embed option to return to start/go up the menu as well as down at any point





##Report on the taxa that were observed in the dataset
def speciesReport(formRecent)
    #Report on taxa spotted on most recent period
    sppRecent = formRecent['2_Species'].unique()        #Extract unique taxa
    obsOld = []
    for i in range(0, len(sppRecent)) :                 #List each species in the dataset
        #Find out if it's a new species or not
        obsOld.append(sum(formOld['2_Species'] == str(sppRecent[i])))
    #Combine into new dataframe
#    sumRecent = pd.DataFrame()
#    sumRecent['Species'] = sppRecent
#    sumRecent['Observations'] = obsOld
#    sumRecent = sumRecent.sort_values(by = 'Observations')      #Sort from least to most commonly observed
    #Print the records
#    print(timeRef, 'you saw', len(sppRecent), 'taxa, which were:')
#    for index, row in sumRecent.iterrows() :
#        if row['Observations'] > 0 :
#            print('    ', row['Species'].upper(), 'which you have seen', row['Observations'], 'times')
#        else :
#            print('    ', row['Species'].upper(), 'which is a NEW RECORD!')






##Species accumulation curves
#For each taxa:
    #plot accumulation through time

##Accumulation curves
obsDays = formComplete['Date'].unique()         #Extract unique dates
obsSppNum = []
for day in obsDays :                            #For each of those days
    formTemp = formComplete['Date'] <= day      #Subset out records up until that day
    obsSppNum.append(len(formTemp['2_Species'].unique()))   #Number of unique species

plot(obsDays, obsSppNum)


for day in obsDays[0:10] :
    print(day)








##Geographic range
#For each species in database:
    #work out area of geog range
    #append column for MaxRangeExtension = 0
    #write to external file
#Read in past geog range file
#For all species observed today:
    #work out new geog range
    #If new species first recorded today:
        #Append to external file
    #else Compare to previous range
    #For species with a range extension:
        #Work out magnitude of range extension
        #Compare magnitude of extension to previous MaxRangeExtension for that species
        #if RecentRangeExtension > MaxRangeExtension for all species 
            #Print 'You have extended the geographic range of XXXX by YYYY km2, which is an alltime record for all species!'
        #elif RecentRangeExtension > MaxRangeExtension for that species
            #Print 'You have extended the geographic range of XXXX by YYYY km2, which is a record range extension for this species'
            #Update external file 
        #else Print 'You have extended the geographic range of XXXX by YYYY km2, but this is not a record'
        #Print the map showing past and present range
        

##Local report
#Get GPS coordinates (from phone or laptop or manuall?)
    #OR: take average coordinate from past day for local area
#Select user-defined buffer
#Select all records from within this buffer
#Generate summary report
    #for each taxon:
        #how many species
        #most common species
        #least common species


#Home coordinates
lat = 51.420443
long = -0.820099
radius = 1000   #search radius in metres




#Convert pandas dataframe to geopandas dataframe
formGDF = gpd.GeoDataFrame(
    formComplete,
    geometry=gpd.points_from_xy(
        formComplete["long_4_GPS_coordinates"],
        formComplete["lat_4_GPS_coordinates"],
    ),
    crs={"init":"EPSG:4326"},
)
#Convert target location to pandas dataframe
target = {'latitude': [lat],
    'longitude': [long]
}
#Convert target location to geopandas dataframe
targetGDF = gpd.GeoDataFrame(
    target, 
    geometry=gpd.points_from_xy(
        target["longitude"],
        target["latitude"],
    ),
    crs={"init":"EPSG:4326"},
)
#Convert both to EPSG:3857 for searching neighbourhood in metres
formGDFproj = formGDF.to_crs({"init": "EPSG:3857"})
targetGDFproj = targetGDF.to_crs({"init": "EPSG:3857"})
#Create buffer around target coordinates
targetBuffer = targetGDFproj.buffer(radius).unary_union
#Find observations that intersect buffer
targetInt = formGDFproj["geometry"].intersection(targetBuffer)










##Hotspots report
#Spatial density of species records
#Map localities
#Report location that has highest density of records
#Report location that has highest number of species for each taxon


##Species report
#User-selected target species
#how often has it been seen; how many localities; map; time series of observations; etc


#Direct import of data from EpiCollect









