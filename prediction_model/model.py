import numpy as np
import tensorflow as tf
import time
from datetime import timedelta
from sklearn.preprocessing import MinMaxScaler
import sys
sys.path.append('..') #unfortunately I can't find a better way to get stuff from sibling folders
from score import get_batch, get_test, get_models, build_test_sets, build_train_sets

import data_loader.loader as loader

def main():
    team_model, player_model = get_models()
    train_keras(team_model, player_model)

def train_keras(team_model, player_model):
    teams = loader.get_games_collection()
    players = loader.get_players_collection()
    names = loader.get_distinct_team_train_names(teams)
    num_batches = len(names)
    minibatches = []
    print("Getting data")
    start = time.time()
    player_set, team_set = build_train_sets(players, teams)
    for num in range(num_batches):
        minibatch = names[num]
        print('Getting data for team: '+str(minibatch))
        data, labels = get_batch(teams, player_set, team_set, player_model, team_model, names[num])
        minibatches.append((minibatch, data, labels))
    end = time.time()
    print("Data gathering done. Time elapsed: " + str(timedelta(seconds = int(end - start))))
    in1 = tf.keras.layers.Input(shape = (2,))
    in2 = tf.keras.layers.Input(shape = (15,1,))
    in3 = tf.keras.layers.Input(shape = (2,))
    in4 = tf.keras.layers.Input(shape = (15,1,))
    flattenh = tf.keras.layers.Flatten()(in2)
    flattena = tf.keras.layers.Flatten()(in4)
    playerh = tf.keras.layers.Dense(64, activation='relu')(flattenh)
    playera = tf.keras.layers.Dense(64, activation='relu')(flattena)
    concath = tf.keras.layers.Concatenate()([in1, playerh])
    concata = tf.keras.layers.Concatenate()([in3, playera])
    teamh = tf.keras.layers.Dense(32, activation='relu')(concath)
    teama = tf.keras.layers.Dense(32, activation='relu')(concata)
    concat = tf.keras.layers.Concatenate()([teamh, teama])
    dense = tf.keras.layers.Dense(16, activation='relu')(concat)
    out = tf.keras.layers.Dense(1, activation='sigmoid')(dense)
    model = tf.keras.Model(inputs=[in1, in2, in3, in4], outputs=[out])
    opt = tf.keras.optimizers.Adam(lr=0.01)
    model.compile(loss='mean_squared_error', optimizer=opt)
    print(model.summary())
    current_batch = 0
    print("Training started")
    start = time.time()
    for i in range(num_batches*300):
        minibatch, data, labels = minibatches[current_batch]
        print('Running batch with players: '+str(minibatch))
        model.train_on_batch([data[0], data[1], data[2], data[3]], labels)
        current_batch = (current_batch + 1)%num_batches
        predictions = model.predict([data])
        print(predictions[0:10])
        print(labels[0:10])
        pct = sum([abs(int(round(predictions[s]))-labels[s]) for s in range(len(predictions))])/len(predictions)
        print("Accuracy: "+ str(pct))
    end = time.time()
    print("Training done. Time elapsed: " + str(timedelta(seconds = int(end - start))))
    # make predictions
    print("Testing started")
    start = time.time()
    player_set, team_set = build_test_sets(players, teams)
    test_data, test_labels = get_test(teams, player_set, team_set, player_model, team_model)
    preds = model.predict([test_data[0], test_data[1], test_data[2], test_data[3]])
    end = time.time()
    print("Testing done. Time elapsed: " + str(timedelta(seconds = int(end - start))))
    pct = sum([abs(int(round(preds[s]))-test_labels[s]) for s in range(len(preds))])/len(preds)
    print("Accuracy: "+ str(pct))
    model_json = model.to_json()
    with open("../prediction_model.json", "w") as json_file:
        json_file.write(model_json)
    model.save_weights("../prediction_model.h5")

if __name__ == '__main__':
    main()