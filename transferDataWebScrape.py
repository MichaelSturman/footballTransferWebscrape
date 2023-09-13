# Data analysis 1 - getting details of players, cost, former nation new nation
# use to generate plots of the flow of player value between leagues over time

import bs4
from bs4 import BeautifulSoup
import pandas as pd
import requests
import re

import warnings
# Bad practice...
# warnings.filterwarnings("ignore")

# summer winter - & for both, s for summer, w for winter
# loan transfer - 1 for all, 2 for only loans, 3 excludes players returning from loan
# 4 excludes loans 
def playerScrape(nation, league, seasonStartYear, summerWinter, loanTransfer):
    
    prevSzn = str(int(seasonStartYear) - 1)[2:] + '/' + seasonStartYear[2:]
    urlStub = 'https://www.transfermarkt.us'

    if nation == 'England':
        if league == 'Prem':
            if int(seasonStartYear) >= 1992:
                urlStem = urlStub + '/premier-league/transfers/wettbewerb/GB1'
            if int(seasonStartYear) < 1992:
                urlStem = urlStub + '/first-division-91-92-/transfers/wettbewerb/EFD1'
        elif league == 'Champshp':
            urlStem = urlStub + '/championship/transfers/wettbewerb/GB2'
        elif league == 'League1':
            urlStem = urlStub + '/league-one/transfers/wettbewerb/GB3'
        elif league == 'League2':
            urlStem = urlStub + '/league-two/transfers/wettbewerb/GB4'
                
    elif nation == 'Germany':
        if league == 'Bundes':
            urlStem = urlStub + '/bundesliga/transfers/wettbewerb/L1'
        elif league == 'Bundes2':
            urlStem = urlStub + '/2-bundesliga/transfers/wettbewerb/L2'
        elif league == 'Bundes3':
            urlStem = urlStub + '/3-bundesliga/transfers/wettbewerb/L3'
    
    elif nation == 'Italy':
        if league == 'SerieA':
            urlStem = urlStub + '/serie-a/transfers/wettbewerb/IT1'
        elif league == 'SerieB':
            urlStem = urlStub + '/serie-b/transfers/wettbewerb/IT2'
        elif league == 'SerieCA':
            urlStem = urlStub + '/serie-c-girone-a/transfers/wettbewerb/IT3A'
        elif league == 'SerieCB':
            urlStem = urlStub + '/serie-c-girone-b/transfers/wettbewerb/IT3B'
        elif league == 'SerieCC':
            urlStem = urlStub + '/serie-c-girone-c/transfers/wettbewerb/IT3C'
    
    elif nation == 'Spain':
        if league == 'LaLiga':
            urlStem = urlStub + '/laliga/transfers/wettbewerb/ES1'
        elif league == 'LaLiga2':
            urlStem = urlStub + '/laliga2/transfers/wettbewerb/ES2'
        elif league == 'PriFedG1':
            urlStem = urlStub + '/primera-division-r-f-e-f-grupo-i/transfers/wettbewerb/E3G1'
        elif league == 'PriFedG2':
            urlStem = urlStub + '/primera-division-r-f-e-f-grupo-ii/transfers/wettbewerb/E3G2'
        elif league == 'PriFedG3':
            urlStem = urlStub + '/primera-division-r-f-e-f-grupo-iii/transfers/wettbewerb/E3G3'

    elif nation == 'France':
        if league == 'Ligue1':
            urlStem = urlStub + '/ligue-1/transfers/wettbewerb/FR1'
        if league == 'Ligue2':
            urlStem = urlStub + '/ligue-2/transfers/wettbewerb/FR2'
        
    url = urlStem + '/plus/?saison_id=' + str(seasonStartYear) + '&s_w=' + summerWinter + 'leihe=' + str(loanTransfer) + '&intern=0&intern=1'

    # Beacause of security of the website the headers section is required
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'}
    soup = BeautifulSoup(requests.get(url, headers=headers).content, 'html5lib')

    cols = {'playerName': [], 'primNat': [], 'seconNat': [], 'pos': [], 'posAbrev': [], 'marketVal': [], 'formClub': [], 'formNation': [], 'newClub': [], 'newNation': [], 'transferCost': []}
    playerData = pd.DataFrame(cols)

    tableBoxes = soup.find_all('div', {'class': 'box'})
    # [print(len(box)) for box in tableBoxes]
    # The boxes of interest are of length 11, rest are filler/other data we don't need

    for box in tableBoxes:  
        if(len(box) == 11):
            team = box.find('h2').find('a').get('title')
            # Make this an argument in future function ^^
            print(team)
            print(box.find('h2').find('a').get('href').split('/'))
            teamUrl = (urlStub + '/' + box.find('h2').find('a').get('href').split('/')[1] + '/platzierungen/verein/' + box.find('h2').find('a').get('href').split('/')[4])
            print(teamUrl)

            # Sub boxes to get in and out tables 
            # first box occupied tableBoxes[3] - swap box for this for any unit tests

            tableSubBoxes = box.find_all('div', {'class': 'responsive-table'})

            for subBox in tableSubBoxes:

                in_out = subBox.find('th', {'class': 'spieler-transfer-cell'}).contents[0]
                tableRows = subBox.find_all('tr')

                # Overall table structure
                # Table Rows 0, 1 --> the season filter
                # Table Row 3 --> filter all transfer, loans, etc
                # Table Row 4 --> filter transfers within club
                # After that, table rows of length 17 --> headers (eg Arsenal in, Arsenal out), 19 --> players

                # Rows of players --> len 19 - 9 rows, rest empty space/new line characters
                # Row 1 - player name (...profil/spieler...) [1]
                # Row 2 - nothing of value [3]
                # Row 3 - player's nationality (or multi) [5]
                # Row 4 - player's position [7]
                # Row 5 - player's position abbreviation [9]
                # Row 6 - transfer market value (euros) [11]
                # Row 7 - club left [13]
                # Row 8 - nation of the club left [15]
                # Row 9 - transfer cost (euros) [17]

                # Number in square braces --> number as shown 

                for row in tableRows:
                    if len(row) == 19:
                        player = (row.find_all('td')[0].find('a').contents[0])
                        #print(player)
                        # how to get the href to navigate to player page - could come in handy later
                        # print(row.find_all('td')[0].find('a').get('href'))
                        nats = [a.get('alt') for a in row.find_all('td')[2].find_all('img')]
                        pos = row.find_all('td')[3].contents[0]
                        posAbrev = row.find_all('td')[4].contents[0]
                        marketVal = row.find_all('td')[5].contents[0]

                        
                        if in_out == 'In':   

                            formerClub = row.find_all('td')[6].find('img').get('alt')
                            #print(row.find_all('td')[6].find('a').get('href'))
                            # There is a number in every team href - if we find this can navigate to placement history
                            #print(row.find_all('td')[6].find('a').get('href').split('/')[4], row.find_all('td')[6].find('a').get('href').split('/')[1])
                            #teamUrl = (urlStub + '/' + row.find_all('td')[6].find('a').get('href').split('/')[1] + '/platzierungen/verein/' + row.find_all('td')[6].find('a').get('href').split('/')[4])
    

                            if row.find_all('td')[7].find('img') != None:
                                formerNat = row.find_all('td')[7].find('img').get('alt')
                            else:
                                formerNat = 'N/A'

                            newClub = team
                            newNat = nation   
                        
                        if in_out == 'Out':
                            
                            formerClub = team
                            formerNat = nation
                            newClub = row.find_all('td')[6].find('img').get('alt')
                            #print(row.find_all('td')[6].find('a').get('href'))

                            if row.find_all('td')[7].find('img') != None:
                                newNat = row.find_all('td')[7].find('img').get('alt')
                                #teamUrl = (urlStub + '/' + row.find_all('td')[6].find('a').get('href').split('/')[1] + '/platzierungen/verein/' + row.find_all('td')[6].find('a').get('href').split('/')[4])                             

                            else:
                                newNat = 'N/A'

                        if len(row.find_all('td')[8].find('a').contents) == 0:
                            transfer == ''   
                        else:
                            transfer = row.find_all('td')[8].find('a').contents[0]

                        #print(player, nats, pos, posAbrev, marketVal, transfer, formerClub, formerNat, newClub, newNat)
                        # May potentially throw an issue when/if we encounter a triple nat. Will cross that bridge
                        # when we come to it
                        # cols = {'playerName': [], 'primNat': [], 'seconNat': [], 'pos': [], 'posAbrev': [], 'marketVal': [], 'formClub': [], 'formClubLeagueLS': [], 'formClubPosLS': [], 'formNation': [], 'newClub': [], 'newClubLeagueLS': [], 'newClubPosLS': [], 'newNation': [], 'transferCost': []}

                        if len(nats) == 2:
                            playerData = pd.concat([playerData, pd.DataFrame.from_records([{'playerName': player, 'primNat': nats[0], 'seconNat': nats[1], 
                                                                                            'pos': pos, 'posAbrev': posAbrev, 'marketVal': marketVal, 
                                                                                            'formClub': formerClub, 'formNation': formerNat, 'newClub': newClub,  
                                                                                            'newNation': newNat, 'transferCost': transfer}])])
                        elif len(nats) == 1:
                            playerData = pd.concat([playerData, pd.DataFrame.from_records([{'playerName': player, 'primNat': nats[0], 'seconNat': 'N/A', 
                                                                                            'pos': pos, 'posAbrev': posAbrev, 'marketVal': marketVal, 
                                                                                            'formClub': formerClub, 'formNation': formerNat, 'newClub': newClub,  
                                                                                            'newNation': newNat, 'transferCost': transfer}])])

    
    playerData.to_csv(nation + '_' + league + '_' + str(seasonStartYear) + '_' + str(loanTransfer) + '.csv', encoding='utf-8-sig')
    return playerData

def main():
    # Supported Nation - England, Leagues - Premier League (use Prem), Championship (use Champshp), League One (use League1),
    # League Two 

    # Supported Nation - Germany, Leagues - Bundesliga (use Bundes) Bundesliga 2 (use Bundes2), Bundesliga 3 (use Bundes3)
    
    # Supported Nation - Italy, Leagues - Serie A (use SerieA), Serie B (use SerieB), Serie C Girone A (use SerieCA),
    # Serie C Girone B (use SerieCB), Serie C Girone C (use SerieCC)
    
    # Supported Nation - Spain, Leagues - La Liga (use LaLiga), La Liga 2 (use LaLiga2), Primera Federacion - Grupo I (PriFedG1),
    # Primera Federacion - Grupo II (PriFedG2), Primera Federacion - Grupo III (PriFedG3)

    # Supported Nation - France, Leagues - Ligue 1 (use Ligue1), Ligue 2 (use Ligue2)

    # summer winter - & for both, s for summer, w for winter
    # loan transfer - 1 for all, 2 for only loans, 3 excludes players returning from loan
    # 4 excludes loans 


    years = range(1983, 2023, 1)
    nations = ('England', 'Spain', 'Italy', 'Germany', 'France')

    for nation in nations:
        if nation == 'England':
            league = 'Prem'
        
        elif nation == 'Spain':
            league = 'LaLiga'

        elif nation == 'Italy':
            league = 'SerieA'

        elif nation == 'Germany':
            league = 'Bundes'
        
        elif nation == 'France':
            league = 'Ligue1'
        
        else:
            print('Error')
        
        print(nation, league)

        for year in years:
            print(year)
            playerScrape(nation, league, str(year), 's', '4')


#playerScrape('England', 'Prem', '2022', 's', '4')

if __name__ == "__main__":
    main()

# Function runs very slowly when we try to get the league/position out as we need to navigate into another webpage for each player... 
# This version ignores league/league pos and just gets team and country - will work on streamlining the other function. It's the opening 
# of all the individual team webpages that causes the issue. Can we do it once at the end? As part of a different funtion?