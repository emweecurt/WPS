import requests
import json
import sys
import datetime

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
    home_team_runs = boxscore['data']['boxscore']['linescore']['home_team_runs']
    away_team_runs = boxscore['data']['boxscore']['linescore']['away_team_runs']
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

    (away_starter, home_starter) = get_game_starters(data)

    # pull game scores
    away_starter_gs = away_starter["game_score"]
    home_starter_gs = home_starter["game_score"]

    # print game scores
    print('Away game score:', away_starter_gs)
    print('Home game score:', home_starter_gs)

    # pull game result
    (away_runs, home_runs) = get_game_runs(data)
    home_won = home_runs > away_runs

    # print game result
    print('Home won?', home_won, "\n")

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

start = datetime.date(2017, 5, 20)
end = datetime.date(2017, 5, 20)
delta = datetime.timedelta(days = 1)
d = start
while d <= end:
    handle_single_day(d)
    d += delta