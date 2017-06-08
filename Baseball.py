import requests
import json
import sys

url = 'http://gd2.mlb.com/components/game/mlb/year_2017/month_05/day_01/gid_2017_05_01_milmlb_slnmlb_1/boxscore.json'
try:
    rawData = requests.get(url, timeout = 2)
except requests.exceptions.Timeout:
    print("Retrieval of data from website timed out.")
    sys.exit()
    
data = rawData.json()

pitch_data = data['data']['boxscore']['pitching']
away_starter = pitch_data[0]['pitcher'][0]
home_starter = pitch_data[1]['pitcher'][0]

