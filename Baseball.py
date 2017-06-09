import requests
import json
import sys

def get_game_starters(boxscore):
    pitch_data = boxscore['data']['boxscore']['pitching']
    away_starter = pitch_data[0]['pitcher'][0]
    home_starter = pitch_data[1]['pitcher'][0]
    return (away_starter, home_starter)

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

game_one = get_game_starters(data)
print(game_one)

