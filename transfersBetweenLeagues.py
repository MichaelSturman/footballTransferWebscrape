import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

englandFull = pd.read_csv('englandFull.csv')
franceFull = pd.read_csv('franceFull.csv')
germanyFull = pd.read_csv('germanyFull.csv')
italyFull = pd.read_csv('italyFull.csv')
spainFull = pd.read_csv('spainFull.csv')

# Only want to show transfers where newNation = nation in question - incoming transfers, 
# and only arrivals from abroad (formNation != naion in question)
englandFull = englandFull[(englandFull.newNation == 'England') & (englandFull.formNation != 'England')].drop('Unnamed: 0', axis=1)
franceFull = franceFull[(franceFull.newNation == 'France') & (franceFull.formNation != 'France')].drop('Unnamed: 0', axis=1)
germanyFull = germanyFull[(germanyFull.newNation == 'Germany') & (germanyFull.formNation != 'Germany')].drop('Unnamed: 0', axis=1)
italyFull = italyFull[(italyFull.newNation == 'Italy') & (italyFull.formNation != 'Italy')].drop('Unnamed: 0', axis=1)
spainFull = spainFull[(spainFull.newNation == 'Spain') & (spainFull.formNation != 'Spain')].drop('Unnamed: 0', axis=1)

# Interested in transfers between these leagues - trim out the others
nations = ['England', 'France', 'Germany', 'Italy', 'Spain']

englandFull = englandFull[(englandFull.formNation == 'France') | (englandFull.formNation == 'Germany') | (englandFull.formNation == 'Italy') |
                          (englandFull.formNation == 'Spain')].reset_index().drop('index', axis=1)

franceFull = franceFull[(franceFull.formNation == 'England') | (franceFull.formNation == 'Germany') | (franceFull.formNation == 'Italy') |
                          (franceFull.formNation == 'Spain')].reset_index().drop('index', axis=1)

germanyFull = germanyFull[(germanyFull.formNation == 'England') | (germanyFull.formNation == 'France') | (germanyFull.formNation == 'Italy') |
                          (germanyFull.formNation == 'Spain')].reset_index().drop('index', axis=1)

italyFull = italyFull[(italyFull.formNation == 'England') | (italyFull.formNation == 'France') | (italyFull.formNation == 'Germany') |
                          (italyFull.formNation == 'Spain')].reset_index().drop('index', axis=1)

spainFull = spainFull[(spainFull.formNation == 'England') | (spainFull.formNation == 'France') | (spainFull.formNation == 'Germany') |
                          (spainFull.formNation == 'Italy')].reset_index().drop('index', axis=1)

#print(englandFull.groupby(['transferYear', 'formNation']).count().newNation)

#allData = pd.concat([englandFull, franceFull, germanyFull, italyFull, spainFull])
#(allData.groupby(['transferYear', 'newNation', 'formNation']).count().playerName.to_csv('data.csv'))

years = np.arange(min(englandFull.transferYear), max(englandFull.transferYear) + 1, 1)

# England
spainE = englandFull[englandFull.formNation == 'Spain']
italyE = englandFull[englandFull.formNation == 'Italy']
franceE = englandFull[englandFull.formNation == 'France']
germanyE = englandFull[englandFull.formNation == 'Germany']

spainCountE = []
italyCountE = []
franceCountE = []
germanyCountE = []

# Spain
englandS = spainFull[spainFull.formNation == 'England']
italyS = spainFull[spainFull.formNation == 'Italy']
franceS = spainFull[spainFull.formNation == 'France']
germanyS = spainFull[spainFull.formNation == 'Germany']

englandCountS = []
italyCountS = []
franceCountS = []
germanyCountS = []

# Italy
englandI = italyFull[italyFull.formNation == 'England']
spainI = italyFull[italyFull.formNation == 'Spain']
franceI = italyFull[italyFull.formNation == 'France']
germanyI = italyFull[italyFull.formNation == 'Germany']

englandCountI = []
spainCountI = []
franceCountI = []
germanyCountI = []

# France
englandF = franceFull[franceFull.formNation == 'England']
spainF = franceFull[franceFull.formNation == 'Spain']
italyF = franceFull[franceFull.formNation == 'Italy']
germanyF = franceFull[franceFull.formNation == 'Germany']

englandCountF = []
spainCountF = []
italyCountF = []
germanyCountF = []

# Germany
englandG = germanyFull[germanyFull.formNation == 'England']
spainG = germanyFull[germanyFull.formNation == 'Spain']
italyG = germanyFull[germanyFull.formNation == 'Italy']
franceG = germanyFull[germanyFull.formNation == 'France']

englandCountG = []
spainCountG = []
italyCountG = []
franceCountG = []

# Groupby and logic giving issues as ignores years where no transfers were made giving a dimensions mismatch when
# trying to plot
for year in years:
    #print(year)
    #print(len(spainE[spainE.transferYear == year].transferYear))
    # England
    spainCountE.append(len(spainE[spainE.transferYear == year].transferYear))
    italyCountE.append(len(italyE[italyE.transferYear == year].transferYear))
    franceCountE.append(len(franceE[franceE.transferYear == year].transferYear))
    germanyCountE.append(len(germanyE[germanyE.transferYear == year].transferYear))

    # Spain
    englandCountS.append(len(englandS[englandS.transferYear == year].transferYear))
    italyCountS.append(len(italyS[italyS.transferYear == year].transferYear))
    franceCountS.append(len(franceS[franceS.transferYear == year].transferYear))
    germanyCountS.append(len(germanyS[germanyS.transferYear == year].transferYear))

    # Italy
    englandCountI.append(len(englandI[englandI.transferYear == year].transferYear))
    spainCountI.append(len(spainI[spainI.transferYear == year].transferYear))
    franceCountI.append(len(franceI[franceI.transferYear == year].transferYear))
    germanyCountI.append(len(germanyI[germanyI.transferYear == year].transferYear))

    # France
    englandCountF.append(len(englandF[englandF.transferYear == year].transferYear))
    spainCountF.append(len(spainF[spainF.transferYear == year].transferYear))
    italyCountF.append(len(italyF[italyF.transferYear == year].transferYear))
    germanyCountF.append(len(germanyF[germanyF.transferYear == year].transferYear))

    # Germany
    englandCountG.append(len(englandG[englandG.transferYear == year].transferYear))
    spainCountG.append(len(spainG[spainG.transferYear == year].transferYear))
    italyCountG.append(len(italyG[italyG.transferYear == year].transferYear))
    franceCountG.append(len(franceG[franceG.transferYear == year].transferYear))

width1=0.2
fig, axs = plt.subplots(5)

print(spainCountF)
font = 5

# England
axs[0].bar(years, spainCountE, color='r', width=width1, label=f'Spain, total: {sum(spainCountE)}')
axs[0].bar(years + width1, italyCountE, color='g', width=width1, label=f'Italy, total: {sum(italyCountE)}')
axs[0].bar(years + 2*width1, franceCountE, color='b', width=width1, label=f'France, total: {sum(franceCountE)}')
axs[0].bar(years + 3*width1, germanyCountE, color='orange', width=width1, label=f'Germany, total: {sum(germanyCountE)}')

axs[0].legend(fontsize=font)
axs[0].title.set_text('England')

# Spain
axs[1].bar(years, englandCountS, color='r', width=width1, label=f'England, total: {sum(englandCountS)}')
axs[1].bar(years + width1, italyCountS, color='g', width=width1, label=f'Italy, total: {sum(italyCountS)}')
axs[1].bar(years + 2*width1, franceCountS, color='b', width=width1, label=f'France, total: {sum(franceCountS)}')
axs[1].bar(years + 3*width1, germanyCountS, color='orange', width=width1, label=f'Germany, total: {sum(germanyCountS)}')

axs[1].legend(fontsize=font)
axs[1].title.set_text('Spain')


# Italy
axs[2].bar(years, englandCountI, color='r', width=width1, label=f'England, total: {sum(englandCountI)}')
axs[2].bar(years + width1, spainCountI, color='g', width=width1, label=f'Spain, total: {sum(spainCountI)}')
axs[2].bar(years + 2*width1, franceCountI, color='b', width=width1, label=f'France, total: {sum(franceCountI)}')
axs[2].bar(years + 3*width1, germanyCountI, color='orange', width=width1, label=f'Germany, total: {sum(germanyCountI)}')

axs[2].legend(fontsize=font)
axs[2].title.set_text('Italy')


# France 
axs[3].bar(years, englandCountF, color='r', width=width1, label=f'England, total: {sum(englandCountF)}')
axs[3].bar(years + width1, spainCountF, color='g', width=width1, label=f'Spain, total: {sum(spainCountF)}')
axs[3].bar(years + 2*width1, italyCountF, color='b', width=width1, label=f'Italy, total: {sum(italyCountF)}')
axs[3].bar(years + 3*width1, germanyCountF, color='orange', width=width1, label=f'Germany, total: {sum(germanyCountF)}')

axs[3].legend(fontsize=font)
axs[3].title.set_text('France')

# Germany
axs[4].bar(years, englandCountG, color='r', width=width1, label=f'England, total: {sum(englandCountG)}')
axs[4].bar(years + width1, spainCountG, color='g', width=width1, label=f'Spain, total: {sum(spainCountG)}')
axs[4].bar(years + 2*width1, italyCountG, color='b', width=width1, label=f'Italy, total: {sum(italyCountG)}')
axs[4].bar(years + 3*width1, franceCountG, color='orange', width=width1, label=f'Germany, total: {sum(franceCountG)}')

axs[4].legend(fontsize=font)
axs[4].title.set_text('Germany')

plt.subplot_tool()
plt.subplots_adjust(left=0.06, bottom=0.08, right=1, top=0.9, wspace=0.2, hspace=1)
plt.show()
plt.close()
