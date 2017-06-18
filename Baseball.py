import requests
import json
import sys

# boxscore: the whole boxscore.json file from gd2.mlb.com for a single game
# returns pitching data for both starting pictchers in a tuple
def get_game_starters(boxscore):
    pitch_data = boxscore['data']['boxscore']['pitching']
    away_starter = pitch_data[0]['pitcher'][0]
    home_starter = pitch_data[1]['pitcher'][0]
    return (away_starter, home_starter)

# boxscore: the whole boxscore.json file from gd2.mlb.com for a single game
# returns number of runs scored by the away team and home team in a tuple
def get_game_runs(boxscore):
    home_team_runs = boxscore['data']['boxscore']['linescore']['home_team_runs']
    away_team_runs = boxscore['data']['boxscore']['linescore']['away_team_runs']
    return (away_team_runs, home_team_runs)

# url: the url to a boxscore.json file
# returns the boxscore as a json object
def fetch_boxscore(url):
    try:
        response = requests.get(url, timeout = 2)
    except requests.exceptions.Timeout:
        print("Retrieval of data from website timed out.")
        return
    if(response.status_code != 200):
        return
    return response.json()

url = 'http://gd2.mlb.com/components/game/mlb/year_2017/month_05/day_01/gid_2017_05_01_milmlb_slnmlb_1/boxscore.json'
data = fetch_boxscore(url)
if(data == None):
    sys.exit()

(away_starter, home_starter) = get_game_starters(data)
#print(game_one)

away_starter_gs = away_starter["game_score"]
home_starter_gs = home_starter["game_score"]

print(away_starter_gs)
print(home_starter_gs)

(away_runs, home_runs) = get_game_runs(data)

home_won = home_runs > away_runs

print(home_won)
