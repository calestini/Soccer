#!/usr/bin/env python2

#League options:
#   Belgium Jupiler League
#   England Premier League
#   France Ligue 1
#   Germany 1. Bundesliga
#   Italy Serie A
#   Netherlands Eredivisie
#   Poland Ekstraklasa
#   Portugal Liga ZON Sagres
#   Scotland Premier League
#   Spain LIGA BBVA
#   Switzerland Super League

import numpy as np
import Load_Datasets as ld
import matplotlib.pyplot as plt

def var_win():

    leagues = [
    'Belgium Jupiler League',
    'England Premier League',
    'France Ligue 1',
    'Germany 1. Bundesliga',
    'Italy Serie A',
    'Spain LIGA BBVA',
    'Portugal Liga ZON Sagres'
    ]

    leagues_data = []

    for i in range(len(leagues)):
        leagues_data_temp,_ = ld.by_league(leagues[i])
        leagues_data.append(leagues_data_temp)

    #print len(leagues_data)

    #EPL,_ = ld.by_league('England Premier League')
    #BJL,_ = ld.by_league('Belgium Jupiler League')
    #FL1,_ = ld.by_league('France Ligue 1')
    #GBL,_ = ld.by_league('Germany 1. Bundesliga')
    #ISA,_ = ld.by_league('Italy Serie A')
    #SLL,_ = ld.by_league('Spain LIGA BBVA')
    #PLZ,_ = ld.by_league('Portugal Liga ZON Sagres')

    var_home = []
    var_away = []
    var_tot = []

    for i in range(len(leagues_data)):
        league_array = np.asarray(leagues_data[i])

        var_home_temp = np.var(league_array[:,9].astype(np.float))
        var_home.append(var_home_temp)

        var_away_temp = np.var(league_array[:,10].astype(np.float))
        var_away.append(var_away_temp)

        var_tot_temp = np.var(league_array[:,8].astype(np.float))
        var_tot.append(var_tot_temp)

    #print var_home
    #print var_away
    #print var_tot
        plot_xref = [1,2,3,4,5,6,7]

    plt.figure(1)
    plt.bar(plot_xref, var_home, align = 'center', color='darkgreen')
    plt.title('Home')
    plt.xlabel('Season')
    plt.ylabel('Variance - Win%')
    plt.xticks(plot_xref, leagues, rotation = 90)
    plt.xlim(0,len(leagues) + 1)
    plt.ylim(0.00,0.05)
    plt.show()


    plt.figure(2)
    plt.bar(plot_xref, var_away, align = 'center', color='darkgreen')
    plt.title('Away')
    plt.xlabel('Season')
    plt.ylabel('Variance - Win%')
    plt.xticks(plot_xref, leagues, rotation = 90)
    plt.xlim(0,len(leagues) + 1)
    plt.ylim(0.00,0.05)
    plt.show()


    plt.figure(3)
    plt.bar(plot_xref, var_tot, align = 'center', color='darkgreen')
    plt.title('Total')
    plt.xlabel('Season')
    plt.ylabel('Variance - Win%')
    plt.xticks(plot_xref, leagues, rotation = 90)
    plt.xlim(0,len(leagues) + 1)
    plt.ylim(0.00,0.05)

    plt.show()

if __name__ == "__main__":
    var_win()
