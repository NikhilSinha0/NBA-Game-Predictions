import sys
import time
from datetime import timedelta
from sklearn.preprocessing import minmax_scale
import hashlib
import numpy as np
sys.path.append('..') #unfortunately I can't find a better way to get stuff from sibling folders

from data_loader.loader import get_games_collection, get_team_batch, get_distinct_test_names, get_team_test, get_distinct_train_names
from data_loader.loader import get_distinct_team_train_names, get_distinct_team_test_names

def get_offensive_defensive_rating(team_json, team_name):
    if team_json["Home"]["Name"]==team_name:
        team = team_json["Home"]
    else:
        team = team_json["Away"]
    return [team["Team Totals"]["ORtg"], team["Team Totals"]["DRtg"]]

def get_game_array_from_json(team_json, team_name):
    game = []

    if team_json["Home"]["Name"]==team_name:
        team = team_json["Home"]
    else:
        team = team_json["Away"]


    for item in team['Team Totals'].keys():
        if item=='MP' or item=='+/-' or item=='USG%':
            continue
        else:
            x = team['Team Totals'][item]
            game.append(x if x!=None else 0)


    if len(team["Last 3 Games Rest"]) == 3:
        average = sum(team["Last 3 Games Rest"])/len(team["Last 3 Games Rest"])
    else:
        temp_arr = team["Last 3 Games Rest"]
        while(len(temp_arr) < 3):
        	temp_arr.append(20)
        average = sum(temp_arr)/len(temp_arr)

    game.append(average)

    game.append(team['Days Rest'] if team['Days Rest']!=None else 0)
    game.append(team['Last 3 Games Distance Travelled']if team['Last 3 Games Distance Travelled']!=None else 0)
    game.append(team['Distance Travelled']if team['Distance Travelled']!=None else 0)

    return game

def get_batch(collection, name):

    print('\n' + "NAME:" + name + '\n')

    indices = []
    data = []
    labels = []
    pad_arr = [0]*get_data_size(collection)
    phash = int(hashlib.md5(name.encode('utf-8')).hexdigest()[:8], 16)%100
    team = get_team_batch(collection, name)

    if(len(team)==0):
        print("")

    # print(get_game_array_from_json(team))
    truncated_data = [get_game_array_from_json(game, name) for game in team]

    # print('\n')
    # print(truncated_data)
    # print('\n')

    #truncated_data = minmax_scale(truncated_data)

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
    labels.extend([get_offensive_defensive_rating(game, name) for game in team])
    return indices, data, labels

def get_test(collection):
    indices = []
    data = []
    labels = []
    pad_arr = [0]*get_data_size(collection)
    for name in get_distinct_team_test_names(collection):
        phash = int(hashlib.md5(name.encode('utf-8')).hexdigest()[:8], 16)%100
        team = get_team_test(collection, name)
        if(len(team)==0):
            print("")
        truncated_data = [get_game_array_from_json(p, name) for p in team]
        #truncated_data = minmax_scale(truncated_data)
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
        labels.extend([get_offensive_defensive_rating(game, name) for game in team])
    return indices, data, labels

def get_data_size(collection):
    recs = collection.find().limit(1)
    record = list(recs)[0]
    return len(record["Home"]["Team Totals"].keys()) + 1

def main():
    # teams = get_teams_collection()
    games = get_games_collection()
    # print(games)
    names = get_distinct_team_train_names(games)
    print(len(names))
    k = 3
    print(names)
    print(names[k])
    start = time.time()
    i, d, l = get_batch(games, names[k])
    end = time.time()
    print(len(i), len(d), len(l))
    print(i[1])
    print(d[1])
    print(l[1])
    print("Done. Time elapsed: " + str(timedelta(seconds = int(end - start))))

if __name__ == '__main__':
    main()
