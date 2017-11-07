import requests
import json
import sys
import datetime
import sqlite3
import matplotlib.pyplot as plt

conn = sqlite3.connect('Pitching_data.db')

c = conn.cursor()

c.execute("PRAGMA foreign_keys = 1")

# boxscore: the whole boxscore.json file from gd2.mlb.com for a single game
# returns pitching data for both starting pictchers in a tuple
def get_game_starters(boxscore):
    pitch_data = boxscore['data']['boxscore']['pitching']

    # check for multiple pitchers
    # if there are multiple pitchers, take the first one
    if type(pitch_data[0]['pitcher']) is list:
        away_starter = pitch_data[0]['pitcher'][0]
    else:
        away_starter = pitch_data[0]['pitcher']

    if type(pitch_data[1]['pitcher']) is list:
        home_starter = pitch_data[1]['pitcher'][0]
    else:
        home_starter = pitch_data[1]['pitcher']

    return (away_starter, home_starter)

# boxscore: the whole boxscore.json file from gd2.mlb.com for a single game
# returns number of runs scored by the away team and home team in a tuple
def get_game_runs(boxscore):
    home_team_runs = int(boxscore['data']['boxscore']['linescore']['home_team_runs'])
    away_team_runs = int(boxscore['data']['boxscore']['linescore']['away_team_runs'])
    return (away_team_runs, home_team_runs)

# url: the url to a json file
# returns the file as a json object
def fetch_json(url):
    try:
        response = requests.get(url, timeout = 2)
    except requests.exceptions.Timeout:
        print("Retrieval of data from website timed out.")
        return
    if(response.status_code != 200):
        return
    return response.json()

# date: date of game
# gid: game id required for url
# prints starters game scores and result of game
def handle_single_game(date, gid):
    print(gid)
    # Construct gd2 URL
    month_padded = date.strftime('%m')
    day_padded = date.strftime('%d')
    url = f"http://gd2.mlb.com/components/game/mlb/year_{date.year}/month_{month_padded}/day_{day_padded}/{gid}/boxscore.json"

    # retrieve json from url
    data = fetch_json(url)
    if(data == None):
        print("No data.", "\n")
        return

    # retrieve pitching data
    (away_starter, home_starter) = get_game_starters(data)

    # determine if home team won
    home_won = 0
    (away_runs, home_runs) = get_game_runs(data)
    if(home_runs > away_runs):
        home_won = 1

    # add game and starters to database
    add_single_game(gid, date.isoformat(), data["data"]["boxscore"]["home_fname"], data["data"]["boxscore"]["away_fname"], data["data"]["boxscore"]["venue_name"], home_won)
    add_single_start(gid, away_starter["name_display_first_last"], away_starter["id"], 0, away_starter["out"], away_starter["h"], away_starter["r"], away_starter["er"], away_starter["hr"], away_starter["bb"], away_starter["so"], away_starter["np"], away_starter["s"], away_starter["bf"], away_starter["game_score"], -1, -1)
    add_single_start(gid, home_starter["name_display_first_last"], home_starter["id"], 1, home_starter["out"], home_starter["h"], home_starter["r"], home_starter["er"], home_starter["hr"], home_starter["bb"], home_starter["so"], home_starter["np"], home_starter["s"], home_starter["bf"], home_starter["game_score"], -1, -1)

# date: date of interest
# returns list of gids for date provided
def get_gids_for_day(date):
    # Construct gd2 URL
    month_padded = date.strftime('%m')
    day_padded = date.strftime('%d')

    url = f"http://gd2.mlb.com/components/game/mlb/year_{date.year}/month_{month_padded}/day_{day_padded}/miniscoreboard.json"

    # retrieve json from url
    data = fetch_json(url)
    if(data == None):
        return
    
    games = data["data"]["games"]["game"]

    # pull gids and return
    return ["gid_" + game["gameday_link"] for game in games]

# date: date of interest
# print results from all games in a single day
def handle_single_day(date):
    gids = get_gids_for_day(date)

    for gid in gids:
        handle_single_game(date, gid)

# DATABASE STUFF

def add_single_start(GameId, PitcherName, PitcherId, IsHomeTeam, Outs, H, R, ER, HR, BB, SO, NP, S, BF, GS, GS_BJ, GS_2):
    PitcherName = PitcherName.replace("'", "")
    c.execute(f'''INSERT INTO starts (GameId, PitcherName, PitcherId, IsHomeTeam, Outs, H, R, ER, HR, BB, SO, NP, S, BF, GS, GS_BJ, GS_2)
        VALUES ('{GameId}', '{PitcherName}',  {PitcherId}, {IsHomeTeam}, {Outs}, {H}, {R}, {ER}, {HR}, {BB}, {SO}, {NP}, {S}, {BF}, {GS}, {GS_BJ}, {GS_2})''')

    conn.commit()

def add_single_game(Id, Date, HomeTeam, AwayTeam, Park, HomeTeamWon):
    c.execute(f'''INSERT INTO games (Id, Date, HomeTeam, AwayTeam, Park, HomeTeamWon)
        VALUES ('{Id}', '{Date}', '{HomeTeam}', '{AwayTeam}', '{Park}', {HomeTeamWon})''')
    
    conn.commit()

# add_single_game('blar', '2017_05_01', 'STL Cardinals', 'ATL Barves', 'Microsoft Field', 1)
# add_single_start('blaz', 'Michael Wacha', 12674, 1, 15, 3, 2, 1, 0, 3, 4, 85, 58, 23, 12, 12, 18)

# start = datetime.date(2016, 4, 3)
# end = datetime.date(2016, 7, 10)
# delta = datetime.timedelta(days = 1)
# d = start
# while d <= end:
#     handle_single_day(d)
#     d += delta

# start = datetime.date(2016, 7, 15)
# end = datetime.date(2016, 10, 2)
# delta = datetime.timedelta(days = 1)
# d = start
# while d <= end:
#     handle_single_day(d)
#     d += delta

game_scores = []
winperstart = []
for gs in range(-18, 105):
    c.execute('SELECT count(*) FROM starts JOIN games on games.Id = GameId WHERE GS == ?', (gs,))
    total = c.fetchone()[0]
    c.execute('SELECT count(*) FROM starts JOIN games on games.Id = GameId WHERE GS == ? AND IsHomeTeam == HomeTeamWon', (gs,))
    wins = c.fetchone()[0]
    if total >= 20:
        WPS = wins/total
        game_scores.append(gs)
        winperstart.append(WPS)
        print('Game score:', gs, 'WPS:', WPS)

plt.plot(game_scores, winperstart, "ro")
plt.title("WPS vs. Game Score")
plt.xlabel("Game score")
plt.ylabel("WPS")
plt.show()