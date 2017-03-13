# -*-coding:utf-8-*-

from sklearn import cross_validation
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingRegressor
from sklearn import metrics

import math
import json
import redis
import pickle


def train_gbdt():
    gbdt=GradientBoostingRegressor(
              loss='ls'
              , learning_rate=0.1
              , n_estimators=200
              , subsample=1
              , min_samples_split=2
              , min_samples_leaf=1
              , max_depth=8
              , init=None
              , random_state=None
              , max_features=None
              , alpha=0.9
              , verbose=0
              , max_leaf_nodes=None
              , warm_start=False
              )

    # filter
    mid_set = set()
    count = 0
    index_set = set()
    with open("mid_list.txt", "r") as f:
        for line in f:
            line = line.strip()
            if line in mid_set:
                index_set.add(count)
            else:
                mid_set.add(line)
            count += 1
    print len(mid_set)

    training_data = []
    count = -1
    with open("feature.txt","r") as f:
        for line in f:
            count += 1
            if count in index_set:
                continue
            line = line.strip()
            line = json.loads(line)
            line[0] = math.log(float(line[0])+1)
            training_data.append(line)

    training_weibo_value = []
    training_uid_value = []
    count = -1
    with open("value.txt","r") as f:
        for line in f:
            count += 1
            if count in index_set:
                continue
            line = line.strip()
            line = json.loads(line)
            training_weibo_value.append((float(line[0])+1))
            training_uid_value.append((float(line[1])+1))

    X_train, X_test, y_train, y_test = cross_validation.train_test_split(training_data, training_uid_value, test_size=0.2, random_state=0)
    print "test: ", len(y_test), len(X_train)
    print "train: ", len(y_train), len(X_test)
    gbdt.fit(X_train, y_train)


    pred = gbdt.predict(X_test)
    ratio = []
    prediction = []
    for i in range(len(y_test)):
        prediction.append(pred[i])
        tmp = y_test[i] - pred[i]
        if tmp >= -10 and tmp <= 10:
            ratio.append(pred[i])
        elif y_test[i]-pred[i] >=-0.2*y_test[i] and y_test[i]-pred[i]<=0.2*y_test[i]:
            ratio.append(pred[i])
    print len(ratio), len(ratio)/float(len(prediction))

    with open("prediction_uid.pkl" ,"wb") as f:
        pickle.dump(gbdt, f)

if __name__ == "__main__":
    train_gbdt()


