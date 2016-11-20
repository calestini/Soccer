#!/usr/bin/env python2

import sqlite3
import numpy as np
import matplotlib.pyplot as plt


def import_dataset(league):
    league_2 = (league,) #create object to be called by sqlite

    with sqlite3.connect('/Users/calestini/Box Sync/Sport Analytics/Soccer/database.sqlite') as db:
        cursor = db.cursor()
        cursor.execute('''SELECT Country.name country
                              , League.name league
                              , Match.season
                              , Match.date
                              , Match.match_api_id
                              , a.team_long_name as home_team_long
                              , a.team_short_name as home_team_short
                              , b.team_long_name as away_team_long
                              , b.team_short_name as away_team_short
                              , Match.home_team_goal
                              , Match.away_team_goal
                              , Match.GBH
                              , Match.GBD
                              , Match.GBA
                              , case when home_team_goal > away_team_goal then 'HOME TEAM'
                                  when away_team_goal > home_team_goal then 'AWAY TEAM'
                                  else 'DRAW' end as winner
                            FROM Match
                              inner join League on Match.league_id = League.id
                              inner join Country on Match.country_id = Country.id
                              inner join (select * from Team) a on Match.home_team_api_id = a.team_api_id
                              inner join (select * from Team) b on Match.away_team_api_id = b.team_api_id
                            WHERE league in (?)
                            ORDER BY Match.date
                            ''', league_2)
        league_matches = []
        counter = 0
        for row in cursor:
        # row[0] returns the first column in the query (name), row[1] returns email column.
            counter += 1
            names = [description[0] for description in cursor.description]
            #if counter == 1:
                #final_dataset.append(names)
            league_matches.append(list(row))
        print '>>> Number of records in dataset: ' + str(counter)
        #print final_dataset

        return league_matches



def by_league(league_name):

    #Retrieve data from database:
    league_matches = import_dataset(league_name)

    ar_league_matches = np.asarray(league_matches)
    #print ar_league_matches

    seasons = np.unique(ar_league_matches[:,2])
    print '>>> Number of seasons available: ' + str(len(seasons))

    teams = np.unique(ar_league_matches[:,5])
    #print '>>> Number of teams in league: ' + str(len(teams))

    league_results = []
    for i in range(len(seasons)):
        teams_in_season = 0
        for j in range(len(teams)):
            home_win_counter = 0.0
            home_draw_counter = 0.0
            home_loss_counter = 0.0
            away_win_counter = 0.0
            away_draw_counter = 0.0
            away_loss_counter = 0.0
            home_games = 0.0
            away_games = 0.0

            for x in range(len(league_matches)):
                #home results:
                if league_matches[x][2] == seasons[i] and league_matches[x][5] == teams[j]:
                    home_games += 1.0
                    if league_matches[x][9] > league_matches[x][10]:
                        home_win_counter += 1.0
                    if league_matches[x][9] == league_matches[x][10]:
                        home_draw_counter += 1.0
                    if league_matches[x][9] < league_matches[x][10]:
                        home_loss_counter += 1.0
                #away results:
                if league_matches[x][2] == seasons[i] and league_matches[x][7] == teams[j]:
                    away_games += 1.0
                    if league_matches[x][9] < league_matches[x][10]:
                        away_win_counter += 1.0
                    if league_matches[x][9] == league_matches[x][10]:
                        away_draw_counter += 1.0
                    if league_matches[x][9] > league_matches[x][10]:
                        away_loss_counter += 1.0
            total_games = home_games + away_games
            total_win = home_win_counter + away_win_counter
            total_draw = home_draw_counter + away_loss_counter
            total_loss = home_loss_counter + away_loss_counter

            if total_games <> 0:
                teams_in_season += 1
                home_win_pct = home_win_counter / home_games
                away_win_pct = away_win_counter / away_games
                total_win_pct = total_win / total_games
                league_results_temp = [seasons[i],teams[j],total_win,total_draw,total_loss,home_games,away_games,total_games, total_win_pct, home_win_pct, away_win_pct]
                league_results.append(league_results_temp)

    #show number of teams in the league:
    #print '>>> Number of team-season combinations :' + str(len(league_results))
    #print '>>> Number of teams: ' + str(teams_in_season)
    #print '>>> Expected number: ' + str(len(seasons)*teams_in_season)

    return league_results, teams_in_season

def plot_league(league_name = 'Belgium Jupiler League', threshold = 0.7, season_plot= '2015/2016'):

    league_results, teams_in_season = by_league(league_name)

    team_plot = []
    team_title = []
    win_pct_plot = []
    team_counter = 0
    for i in range(len(league_results)):
        if season_plot == league_results[i][0]:
            team_counter += 1
            team_title.append(league_results[i][1])
            team_plot.append(team_counter)
            win_pct_plot.append(league_results[i][8])

    #print team_plot
    #print win_pct_plot
    #print np.var(np.asarray(win_pct_plot))

    plt.figure()
    plt.bar(team_plot, win_pct_plot, align = 'center', color='darkgreen')
    plt.title('League: ' + league_name + '  -  Season: ' + season_plot)
    plt.xlabel('Team')
    plt.ylabel('Win%')
    plt.xticks(team_plot, team_title, rotation = 90)
    plt.xlim(0,teams_in_season + 1)
    plt.ylim(0.00,1.00)
    plt.axhline(y=threshold, xmin=0, xmax=1, hold=None, color = 'r', ls = 'dotted')

    plt.show()


if __name__ == "__main__":
    plot_league(league_name = 'Belgium Jupiler League', threshold = 0.7, season_plot = '2015/2016')

