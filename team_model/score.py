import sys
import time
from datetime import timedelta
from sklearn.preprocessing import minmax_scale
import hashlib
import numpy as np
sys.path.append('..') #unfortunately I can't find a better way to get stuff from sibling folders

from data_loader.loader import get_games_collection, get_team_batch, get_distinct_test_names, get_team_test, get_distinct_train_names

def get_offensive_defensive_rating(team_json):
    return [team_json["ORtg"], team_json["DRtg"]]

def get_game_array_from_json(team_json):
    game = []
    for item in team_json['Team Totals'].keys():
        if item=='MP' or item=='+/-':
            continue
        else:
            x = team_json[item]
            game.append(x if x!=None else 0)
    game.append(sum(team_json["Last 3 Games Rest"])/len(team_json["Last 3 Games Rest"]))
    games.append(team_json['Days Rest'])
    games.append(team_json['Last 3 Games Distance Travelled'])
    games.append(team_json['Distance Travelled'])
    return game

def get_batch(collection, name):
    indices = []
    data = []
    labels = []
    pad_arr = [0]*get_data_size(collection)
    phash = int(hashlib.md5(name.encode('utf-8')).hexdigest()[:8], 16)%100
    team = get_team_batch(collection, name)
    if(len(team)==0):
        continue
    truncated_data = [get_game_array_from_json(p) for p in team]
    truncated_data = minmax_scale(truncated_data)
    indices.extend([phash]*len(team))
    team_data = []
    for k in range(len(truncated_data)):
        if k < 5:
            arr = [np.array(pad_arr)]*(5-k)
            arr.extend(truncated_data[0:k])
        else:
            arr = truncated_data[k-5:k]
        team_data.append(arr)
    data.extend(team_data)
    labels.extend([get_offensive_defensive_rating(game) for game in team])
    return indices, data, labels

def get_test(collection):
    indices = []
    data = []
    labels = []
    pad_arr = [0]*get_data_size(collection)
    phash = int(hashlib.md5(name.encode('utf-8')).hexdigest()[:8], 16)%100
    team = get_team_test(collection, name)
    if(len(team)==0):
        continue
    truncated_data = [get_game_array_from_json(p) for p in team]
    truncated_data = minmax_scale(truncated_data)
    indices.extend([phash]*len(team))
    team_data = []
    for k in range(len(truncated_data)):
        if k < 5:
            arr = [np.array(pad_arr)]*(5-k)
            arr.extend(truncated_data[0:k])
        else:
            arr = truncated_data[k-5:k]
        team_data.append(arr)
    data.extend(team_data)
    labels.extend([get_offensive_defensive_rating(game) for game in team])
    return indices, data, labels

def get_data_size(collection):
    recs = collection.find().limit(1)
    record = list(recs)[0]
    return len(record["Team Totals"].keys())+2

def main():
    teams = get_teams_collection()
    names = get_distinct_train_names(teams)
    k = 3
    print(names[k])
    start = time.time()
    i, d, l = get_batch(teams, names[k])
    end = time.time()
    print(len(i), len(d), len(l))
    print(i[1])
    print(d[1])
    print(l[1])
    print("Done. Time elapsed: " + str(timedelta(seconds = int(end - start))))

if __name__ == '__main__':
    main()