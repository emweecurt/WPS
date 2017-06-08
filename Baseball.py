import requests
import json

# url = 'http://gd2.mlb.com/components/game/mlb/year_2017/month_05/day_01/gid_2017_05_01_milmlb_slnmlb_1/boxscore.json'

# rawData = requests.get(url)
# print(rawData)
# print(rawData.json())

with open('sample_data.json') as data_file:
    data = json.load(data_file)

print(data)

pitch_data = data['data']['boxscore']['pitching']
away_starter = pitch_data[0]['pitcher'][0]
home_starter = pitch_data[1]['pitcher'][0]
