import sys
import time
from datetime import timedelta
from sklearn.preprocessing import minmax_scale
import hashlib
import numpy as np
import tensorflow.keras.models as models
sys.path.append('..') #unfortunately I can't find a better way to get stuff from sibling folders

import data_loader.loader as loader
from team_model.score import get_game_array_from_json
from player_model.score import get_data_size as get_player_data_size
from team_model.score import get_data_size as get_team_data_size

def get_output(team_json):
    return [team_json["Home"]["Win"]]

def get_predictions_from_json(players, teams, player_model, team_model, game_json):
    away = []
    home = []
    date = game_json["Date"]
    p = []
    i = []
    for player in game_json["Home"]["Players"]:
        if(not date in players[player["Name"]]):
            #print("Could not find " + date + " in player " + player["Name"])
            continue
        p.append(players[player["Name"]][date][1])
        i.append(players[player["Name"]][date][0])
    home = model_predict(player_model, i, p).tolist()
    while(len(home)<15):
        home.append([0])
    home_team_prediction = model_predict(team_model, [teams[game_json["Home"]["Name"]][date][0]], [teams[game_json["Home"]["Name"]][date][1]])
    for player in game_json["Away"]["Players"]:
        if(not date in players[player["Name"]]):
            #print("Could not find " + date + " in player " + player["Name"])
            continue
        p.append(players[player["Name"]][date][1])
        i.append(players[player["Name"]][date][0])
    away = model_predict(player_model, i, p).tolist()
    while(len(away)<15):
        away.append([0])
    away_team_prediction = model_predict(team_model, [teams[game_json["Away"]["Name"]][date][0]], [teams[game_json["Away"]["Name"]][date][1]])
    return [home, home_team_prediction, away, away_team_prediction]

def build_train_sets(player_collection, team_collection):
    players = {}
    teams = {}
    pad_arr = [0]*get_team_data_size(team_collection)
    for name in loader.get_distinct_team_train_names(team_collection):
        print("Building set for team: " + name)
        teams[name] = {}
        phash = int(hashlib.md5(name.encode('utf-8')).hexdigest()[:8], 16)%100
        team = loader.get_team_batch(team_collection, name)
        if(len(team)==0):
            continue
        truncated_data = [get_game_array_from_json(p, name) for p in team]
        #truncated_data = minmax_scale(truncated_data)
        team_data = []
        for k in range(len(truncated_data)):
            if k < 5:
                arr = [np.array(pad_arr)]*(5-k)
                arr.extend(truncated_data[0:k])
            else:
                arr = truncated_data[k-5:k]
            teams[name][team[k]["Date"]] = [phash, arr]
    pad_arr = [0]*get_player_data_size(player_collection)
    for name in loader.get_distinct_train_names(player_collection):
        print("Building set for player: " + name)
        players[name] = {}
        phash = int(hashlib.md5(name.encode('utf-8')).hexdigest()[:8], 16)%10000
        player = loader.get_partial_batch(player_collection, name)
        if(len(player)==0):
            continue
        truncated_data = [[x if x!=None else 0 for x in list(p.values())[3:]] for p in player]
        #truncated_data = minmax_scale(truncated_data)
        player_data = []
        for k in range(len(truncated_data)):
            if k < 5:
                arr = [np.array(pad_arr)]*(5-k)
                arr.extend(truncated_data[0:k])
            else:
                arr = truncated_data[k-5:k]
            players[name][player[k]["Date"]] = [phash, arr]
    return players, teams

def build_test_sets(player_collection, team_collection):
    players = {}
    teams = {}
    pad_arr = [0]*get_team_data_size(team_collection)
    for name in loader.get_distinct_team_test_names(team_collection):
        print("Building set for team: " + name)
        teams[name] = {}
        phash = int(hashlib.md5(name.encode('utf-8')).hexdigest()[:8], 16)%100
        team = loader.get_team_test(team_collection, name)
        if(len(team)==0):
            continue
        truncated_data = [get_game_array_from_json(p, name) for p in team]
        #truncated_data = minmax_scale(truncated_data)
        team_data = []
        for k in range(len(truncated_data)):
            if k < 5:
                arr = [np.array(pad_arr)]*(5-k)
                arr.extend(truncated_data[0:k])
            else:
                arr = truncated_data[k-5:k]
            teams[name][team[k]["Date"]] = [phash, arr]
    pad_arr = [0]*get_player_data_size(player_collection)
    for name in loader.get_distinct_test_names(player_collection):
        print("Building set for player: " + name)
        players[name] = {}
        phash = int(hashlib.md5(name.encode('utf-8')).hexdigest()[:8], 16)%10000
        player = loader.get_partial_test(player_collection, name)
        if(len(player)==0):
            continue
        truncated_data = [[x if x!=None else 0 for x in list(p.values())[3:]] for p in player]
        #truncated_data = minmax_scale(truncated_data)
        player_data = []
        for k in range(len(truncated_data)):
            if k < 5:
                arr = [np.array(pad_arr)]*(5-k)
                arr.extend(truncated_data[0:k])
            else:
                arr = truncated_data[k-5:k]
            player_data.append(arr)
        players[name][player[k]["Date"]] = [phash, arr]
    return players, teams

def model_predict(model, indices, data):
    pred = model.predict([indices, data])
    return pred

def get_batch(team_collection, players, teams, player_model, team_model, name):
    home_team, home_player, away_team, away_player = [], [], [], []
    labels = []
    team = loader.get_team_home_batch(team_collection, name)
    for p in team:
        preds = get_predictions_from_json(players, teams, player_model, team_model, p)
        home_team.append(preds[0])
        home_player.append(preds[1])
        away_team.append(preds[2])
        away_player.append(preds[3])
    labels.extend([get_output(game) for game in team])
    return [home_team, home_player, away_team, away_player], labels

def get_test(team_collection, players, teams, player_model, team_model):
    home_team, home_player, away_team, away_player = [], [], [], []
    labels = []
    for name in loader.get_distinct_team_test_names(team_collection):
        team = loader.get_team_home_test(team_collection, name)
        if(len(team)==0):
            continue
        for p in team:
            preds = get_predictions_from_json(players, teams, player_model, team_model, p)
            home_team.append(preds[0])
            home_player.append(preds[1])
            away_team.append(preds[2])
            away_player.append(preds[3])
        labels.extend([get_output(game) for game in team])
    return [home_team, home_player, away_team, away_player], labels

def get_models():
    team_json_file = open('../team_model.json', 'r')
    team_model_json = team_json_file.read()
    team_json_file.close()
    team_model = models.model_from_json(team_model_json)
    team_model.load_weights("../team_model.h5")
    player_json_file = open('../player_model.json', 'r')
    player_model_json = player_json_file.read()
    player_json_file.close()
    player_model = models.model_from_json(player_model_json)
    player_model.load_weights("../player_model.h5")
    return team_model, player_model

def main():
    teams = loader.get_teams_collection()
    players = loader.get_players_collection()
    team_model, player_model = get_models()
    names = get_distinct_train_names(teams)
    k = 3
    print(names[k])
    start = time.time()
    d, l = get_batch(players, teams, player_model, team_model, names[k])
    end = time.time()
    print(len(d), len(l))
    print(d[1])
    print(l[1])
    print("Done. Time elapsed: " + str(timedelta(seconds = int(end - start))))

if __name__ == '__main__':
    main()