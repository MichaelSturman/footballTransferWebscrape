import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import re

# Suppress warning that arrises when trying to reformat transfer cost
pd.options.mode.chained_assignment = None  # default='warn'


years = range(1983, 2023)

csvNamesEng = ['England_Prem_' + str(year) + '_4.csv' for year in years]
csvNamesSp = ['Spain_LaLiga_' + str(year) + '_4.csv' for year in years]
csvNamesGe = ['Germany_Bundes_' + str(year) + '_4.csv' for year in years]
csvNamesIt = ['Italy_SerieA_' + str(year) + '_4.csv' for year in years]
csvNamesFr = ['France_Ligue1_' + str(year) + '_4.csv' for year in years]

cols = {'playerName': [], 'primNat': [], 'seconNat': [], 'pos': [], 'posAbrev': [], 'marketVal': [], 'formClub': [], 'formNation': [], 'newClub': [], 'newNation': [], 'transferCost': []}
englandFull = spainFull = germanyFull = italyFull = franceFull = pd.DataFrame(cols)


for year in range(1983, 2023):
    csvNameEng = 'England_Prem_' + str(year) + '_4.csv' 
    csvNameSpa = 'Spain_LaLiga_' + str(year) + '_4.csv' 
    csvNameGer = 'Germany_Bundes_' + str(year) + '_4.csv' 
    csvNameIta = 'Italy_SerieA_' + str(year) + '_4.csv' 
    csvNameFra = 'France_Ligue1_' + str(year) + '_4.csv'

    eng = pd.read_csv(csvNameEng)
    spa = pd.read_csv(csvNameSpa)
    ger = pd.read_csv(csvNameGer)
    ita = pd.read_csv(csvNameIta)
    fra = pd.read_csv(csvNameFra)  

    eng['transferYear'] = spa['transferYear'] = ger['transferYear'] = ita['transferYear'] = fra['transferYear'] = str(year)

    # Weird extra column has snuck in. Get rid
    englandFull = pd.concat([englandFull, eng])

    spainFull = pd.concat([spainFull, spa])

    germanyFull = pd.concat([germanyFull, ger])

    italyFull = pd.concat([italyFull, ita])

    franceFull = pd.concat([franceFull, fra])

# Transfer data has been put into dataframes for each nation. Now some data cleaning
# transferCost column has some non numeric options - free transfer, loan transfer, end of loan, ?, '-'
# drop the rows with loan transfer and end of loan. free transfer map to 0, ? leave as is for now, '-' to 0
# transfer values are given in €500k, or €2.50m [2 decimal places] - convert to integers 

def dataClean(dataFrame, fileName):

    # Getting rid of rows that contain loan/end of loan transfers. Also includes loan fees (shows as 'Loan fee:' with no actual fee value)
    # Not interested in this
    dataFrame = dataFrame[dataFrame.transferCost != 'loan transfer']
    dataFrame = dataFrame[dataFrame.transferCost != 'End of loan']
    dataFrame = dataFrame[dataFrame.transferCost != 'Loan fee:']

    # Replacing free and - with 0.00
    dataFrame = dataFrame.replace(['free transfer', '-'], 0.00)

    # Reset the index having dropped rows
    dataFrame = dataFrame.reset_index()

    # We have a few columns to get rid of - one called 'Unnamed: 0' and the other 'index' (old index from the merged csvs, defunct as non-unique. we have already
    # replaced above)
    dataFrame = dataFrame.drop(['Unnamed: 0', 'index'], axis=1)

    # Reformatting transferCost to be consistent
    indMil = [index for index in dataFrame[dataFrame['transferCost'].str.endswith('m').fillna(False)].index]
    indThou = [index for index in dataFrame[dataFrame['transferCost'].str.endswith('k').fillna(False)].index]

    for ind in indMil:
        dataFrame.transferCost.loc[ind] = float(dataFrame.transferCost.loc[ind][1:-1]) * 10**6

    for ind in indThou:
        dataFrame.transferCost.loc[ind] = float(dataFrame.transferCost.loc[ind][1:-1]) * 10**3

    # The method used above missed out a few players who were sold for fees of less than a thousand Euros.
    # Having dealt with the millions and thousands all the strings remaining with € at the start will be > 1000,
    # so we can use € as our search criteria

    indHun = [index for index in dataFrame[dataFrame['transferCost'].str.startswith('€').fillna(False)].index]

    for ind in indHun:
        dataFrame.transferCost.loc[ind] = float(dataFrame.transferCost.loc[ind][1:])

    # Same reformatting has to be done for market val, but no text strings to replace. All either 0 or XYZk/XYZm
    indMil = [index for index in dataFrame[dataFrame['marketVal'].str.endswith('m').fillna(False)].index]
    indThou = [index for index in dataFrame[dataFrame['marketVal'].str.endswith('k').fillna(False)].index]

    for ind in indMil:
        dataFrame.marketVal.loc[ind] = float(dataFrame.marketVal.loc[ind][1:-1]) * 10**6

    for ind in indThou:
        dataFrame.marketVal.loc[ind] = float(dataFrame.marketVal.loc[ind][1:-1]) * 10**3

    #print(dataFrame[dataFrame.transferCost != '?'].groupby(['transferYear']).count().transferCost/dataFrame.groupby(['transferYear']).count().transferCost)
    #print(dataFrame[dataFrame.transferCost != '?'].groupby('transferYear').count().transferCost)

    # Earlier data up to half of the transfers are missing the cost, leaving less than 150 players with data populated. Still leaves enough 
    # data to extract insights from though and I don't see a way of filling the blanks. Will look to drop '?' data.
    #dataFrame = dataFrame.drop(dataFrame[dataFrame.transferCost == '?'].index)

    # Some types of move don't interest us - we can drop rows where new club =
    # Retired, Unknown, Career Break or Without Club
    indClub = dataFrame[(dataFrame.newClub == 'Retired') | (dataFrame.newClub == 'Career Break') | (dataFrame.newClub == 'Unknown') | (dataFrame.newClub == 'Without Club')].index
    dataFrame = dataFrame.drop(indClub)


    # Also not interested in players where new club == former club (eg players coming up from academy)
    # Also have former club = XYZ + ' U18. Struggling to get rid of this
    indProm = dataFrame[(dataFrame.newClub == dataFrame.formClub)].index
    dataFrame = dataFrame.drop(indProm)

    # Players with form club as unknown --> form nation --> unknown, same for new club/new nation.
    # The below fills in some data for other situations - 'Career Break', 'Without Club', 'Disqualification' and 'Unknown'
    dataFrame.formNation = dataFrame.formNation.fillna('N/A')
    dataFrame.newNation = dataFrame.newNation.fillna('N/A')



    #print(dataFrame[dataFrame.marketVal > 0].groupby('transferYear').count().marketVal)
    # Market value data only really begins to get populated in any meaninful fraction (>50%) in 2015.
    # Incomplete column, should drop. 
    # For current purposes also won't get any value out of seconNat, posAbrev. Drop these too.
    dataFrame = dataFrame.drop(['marketVal', 'seconNat', 'posAbrev'], axis=1)

    # We are looking to analyse trends within the movement of players between Europes current top 5 leagues
    # England, Spain, Germany, Italy and France. Each transfer between two of these nations will show as an in
    # for one nation and an out for another. We'll just be paying attention to incomings to avoid double counting.
    # We can trim down our data by looking in the formNations column for any of the big 5 and removing others.
    # Then we will double over and remove rows with the same newNation and formNation.

    dataFrame.to_csv(fileName + '.csv', encoding='utf-8-sig')




dataClean(englandFull, 'englandFull')
dataClean(spainFull, 'spainFull')
dataClean(germanyFull, 'germanyFull')
dataClean(italyFull, 'italyFull')
dataClean(franceFull, 'franceFull')



