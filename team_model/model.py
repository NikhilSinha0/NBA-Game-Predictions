import numpy as np
import tensorflow as tf
import time
from datetime import timedelta
from sklearn.preprocessing import MinMaxScaler
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
    collection = loader.get_games_collection()
    names = loader.get_distinct_train_names(collection)
    # num_batches = (len(names)//10)+1
    num_batches = (len(names)) +1

    data_size = get_data_size(collection)
    minibatches = []
    print("Getting data")
    start = time.time()
    for num in range(num_batches):
        # minibatch = names[10*num:10*(num+1)]
        minibatch = names[num]
        print('Getting data for players: '+str(minibatch))
        indices, data, labels = get_batch(collection, minibatch)
        minibatches.append((minibatch, indices, data, labels))
    end = time.time()
    print("Data gathering done. Time elapsed: " + str(timedelta(seconds = int(end - start))))
    in1 = tf.keras.layers.Input(shape = (1,))
    in2 = tf.keras.layers.Input(shape = (5, data_size,))
    # embed = tf.keras.layers.Embedding(10000, 64, input_length=1)(in1)
    embed = tf.keras.layers.Embedding(100, 64, input_length=1)(in1)
    flat_embed = tf.keras.layers.Reshape((64,))(embed)
    shaped = tf.keras.layers.RepeatVector(5)(flat_embed)
    concat = tf.keras.layers.Concatenate(axis=2)([shaped, in2])
    lstm = tf.keras.layers.LSTM(64)(concat)
    dense = tf.keras.layers.Dense(16, activation='relu')(lstm)
    out = tf.keras.layers.Dense(2, activation='sigmoid')(dense)
    model = tf.keras.Model(inputs=[in1, in2], outputs=[out])
    opt = tf.keras.optimizers.Adam(lr=0.01)
    model.compile(loss='mean_absolute_error', optimizer=opt)
    print(model.summary())
    current_batch = 0
    print("Training started")
    start = time.time()
    for i in range(num_batches*300):
        minibatch, indices, data, labels = minibatches[current_batch]
        print('Running batch with players: '+str(minibatch))
        labels_scaler = MinMaxScaler(feature_range=(0, 1))
        labels_normalized = labels_scaler.fit_transform(labels)
        model.train_on_batch([indices, data], labels_normalized)
        current_batch = (current_batch + 1)%num_batches
        predictions_normal = model.predict([indices, data])
        predictions = labels_scaler.inverse_transform(predictions_normal)
        print(predictions[0:10])
        print(labels[0:10])
        avg_err = sum([abs(predictions[s]-labels[s]) for s in range(len(predictions))])/len(predictions)
        pct_within_1 = sum([1 if abs(predictions[s]-labels[s])<1 else 0 for s in range(len(predictions))])/len(predictions)
        print("Average error: "+ str(avg_err))
        print("Percent within 1: "+ str(pct_within_1))
    end = time.time()
    print("Training done. Time elapsed: " + str(timedelta(seconds = int(end - start))))
    # make predictions
    print("Testing started")
    start = time.time()
    test_ind, test_data, test_labels = get_test(collection)
    test_labels_scaler = MinMaxScaler(feature_range=(0, 1))
    test_labels_normalized = test_labels_scaler.fit_transform(labels)
    preds_normal = model.predict([test_ind, test_data])
    preds = test_labels_scaler.inverse_transform(preds_normal)
    end = time.time()
    print("Testing done. Time elapsed: " + str(timedelta(seconds = int(end - start))))
    avg_err = sum([abs(preds[s]-test_labels[s]) for s in range(len(preds))])/len(preds)
    pct_within_1 = sum([1 if abs(preds[s]-test_labels[s])<1 else 0 for s in range(len(preds))])/len(preds)
    print("Average error: "+ str(avg_err))
    print("Percent within 1: "+ str(pct_within_1))

if __name__ == '__main__':
    main()
