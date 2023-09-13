import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

englandFull = pd.read_csv('englandFull.csv')
franceFull = pd.read_csv('franceFull.csv')
germanyFull = pd.read_csv('germanyFull.csv')
italyFull = pd.read_csv('italyFull.csv')
spainFull = pd.read_csv('spainFull.csv')

print(englandFull[englandFull.formNation == 'England'].playerName.count(), englandFull[englandFull.formNation != 'England'].playerName.count())

years = np.arange(min(englandFull.transferYear), max(englandFull.transferYear) + 1, 1)

transferFracEng = []
transferFracFra = []
transferFracGer = []
transferFracIta = []
transferFracSpa = []

for year in years:

    engFrac = (englandFull[(englandFull.formNation != 'England') & (englandFull.transferYear == year)].playerName.count() / 
                englandFull[(englandFull.transferYear == year)].playerName.count())
    transferFracEng.append(engFrac)
    
    fraFrac = (franceFull[(franceFull.formNation != 'France') & (franceFull.transferYear == year)].playerName.count()/ 
            franceFull[(franceFull.transferYear == year)].playerName.count())
    transferFracFra.append(fraFrac)
    
    gerFrac = (germanyFull[(germanyFull.formNation != 'Germany') & (germanyFull.transferYear == year)].playerName.count()/ 
            germanyFull[(germanyFull.transferYear == year)].playerName.count())
    transferFracGer.append(gerFrac)
    
    itaFrac = (italyFull[(italyFull.formNation != 'Italy') & (italyFull.transferYear == year)].playerName.count()/ 
            italyFull[(italyFull.transferYear == year)].playerName.count())
    transferFracIta.append(itaFrac)
    
    spaFrac = (spainFull[(spainFull.formNation != 'Spain') & (spainFull.transferYear == year)].playerName.count()/ 
            spainFull[(spainFull.transferYear == year)].playerName.count())
    transferFracSpa.append(spaFrac)
    
fig, axs = plt.subplots(5)
font = 5

axs[0].plot(years, transferFracEng, color='red')
axs[0].title.set_text('England')

axs[1].plot(years, transferFracFra, color='blue')
axs[1].title.set_text('France')

axs[2].plot(years, transferFracGer, color='black')
axs[2].title.set_text('Germany')

axs[3].plot(years, transferFracIta, color='green')
axs[3].title.set_text('Italy')

axs[4].plot(years, transferFracSpa, color='orange')
axs[4].title.set_text('Spain')

plt.subplots_adjust(left=0.06, bottom=0.08, right=1, top=0.9, wspace=0.2, hspace=1)
plt.show()