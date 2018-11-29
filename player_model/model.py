import numpy as np
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
import time
from datetime import timedelta
#from sklearn.metrics import mean_squared_error
import sys
sys.path.append('..') #unfortun0ately I can't find a better way to get stuff from sibling folders
from score import get_batch, get_test, get_data_size

import data_loader.loader as loader

def main():
    train_keras()

def train_keras():
    # create and fit the LSTM network
    # model = tf.keras.models.Sequential()
    # model.add(tf.keras.layers.Embedding(10000, 64))
    # model.add(tf.keras.layers.concatenate())
    # model.add(tf.keras.layers.LSTM(5, input_shape=(1, 5)))
    # model.add(tf.keras.layers.Dense(1, activation='sigmoid'))
    collection = loader.get_players_collection()
    names = loader.get_distinct_train_names(collection)
    num_batches = (len(names)//10)+1
    data_size = get_data_size(collection)

    in1 = tf.keras.layers.Input(shape = (1,))
    in2 = tf.keras.layers.Input(shape = (data_size,))
    embed = tf.keras.layers.Embedding(10000, 64, input_length=1)(in1)
    shaped = tf.keras.layers.Reshape((1, data_size,))(in2)
    concat = tf.keras.layers.Concatenate(axis=2)([shaped, embed])
    lstm = tf.keras.layers.LSTM(64)(concat)
    dense = tf.keras.layers.Dense(16, activation='relu')(lstm)
    out = tf.keras.layers.Dense(1, activation='sigmoid')(dense)
    model = tf.keras.Model(inputs=[in1, in2], outputs=[out])
    model.compile(loss='mean_squared_error', optimizer='adam')
    print(model.summary())
    current_batch = 0
    print("Training started")
    start = time.time()
    for i in range(num_batches*100):
        print('Running batch with players: '+str(names[10*current_batch:10*(current_batch+1)]))
        indices, data, labels = get_batch(collection, names[10*current_batch:10*(current_batch+1)])
        data_scaler = MinMaxScaler(feature_range=(0, 1))
        data = data_scaler.fit_transform(data)
        labels_scaler = MinMaxScaler(feature_range=(0, 1))
        labels = labels_scaler.fit_transform(labels)
        model.train_on_batch([indices, data], labels)
        current_batch = (current_batch + 1)%num_batches
        raw_predictions = model.predict([indices, data])
        predictions = labels_scaler.inverse_transform(raw_predictions)
        labels = labels_scaler.inverse_transform(labels)
        print(predictions[0:10])
        print(labels[0:10])
        avg_err = sum([abs(predictions[s]-labels[s]) for s in range(len(predictions))])
    end = time.time()
    print("Training done. Time elapsed: " + str(timedelta(seconds = int(end - start))))
    # make predictions
    print("Getting test set")
    test_ind, test_data, test_labels = get_test(collection)
    print("Training started")
    start = time.time()
    data_scaler = MinMaxScaler(feature_range=(0, 1))
    test_data = data_scaler.fit_transform(test_data)
    labels_scaler = MinMaxScaler(feature_range=(0, 1))
    test_labels = labels_scaler.fit_transform(test_labels)
    raw_preds = model.predict([test_ind, test_data])
    preds = labels_scaler.inverse_transform(raw_preds)
    end = time.time()
    print("Testing done. Time elapsed: " + str(timedelta(seconds = int(end - start))))
    avg_err = sum([abs(preds[s]-test_labels[s]) for s in range(len(preds))])
    print("Average error: "+ str(avg_err))

if __name__ == '__main__':
    main()