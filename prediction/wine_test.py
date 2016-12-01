import os
import json
import time
import pickle
import requests

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

CONSTANTS = {
              'redurl': "http://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv"
            , 'whiteurl': "http://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-white.csv"
            , 'redpath': "./wine_data/winequality-red.csv"
            , 'whitepath': "./wine_data/winequality-white.csv"
            , 'readme': "./wine_data/winequality.names"
    }

print(CONSTANTS['redurl'])

#The data is in a csv file but uses semicolon seperators. It also has header names embedded in the first row of the file.
#We can use the read_csv method to easily load the data into a dataframe.
dfwine = pd.read_csv(CONSTANTS['redpath'], sep=';')

#Let's prep our data
from sklearn.datasets.base import Bunch

#This function takes a dataframe of our raw data, cleans it and puts it in a Bunch
def prepdata(df):

    filenames = CONSTANTS

    #Our feature names can be pulled from our dataframe, but we don't want the last column because this is our target
    feature_names = list(df.columns.values)
    del feature_names[-1]
    target_names=["quality"]

    #We can use feature_names as a way to convert the dataframe to a numpy array, excluding the last column
    data = df.as_matrix(feature_names)
    #Our target is just the last column
    target = df['quality'].as_matrix()

    with open(filenames['readme'], 'r') as f:
        DESCR = f.read()

    return Bunch(
        data=data,
        target=target,
        filenames=filenames,
        target_names=target_names,
        feature_names=feature_names,
        DESCR=DESCR
    )
dataset = prepdata(dfwine)

print(dataset.data.shape)
print(dataset.target.shape)

print(dataset['feature_names'])
print(dataset['data'])
print(dataset['target_names'])

print(dataset['target'])

##################################################
from sklearn import metrics
from sklearn import cross_validation
from sklearn.cross_validation import KFold

import train_models
modeler = train_models.ManyModels()
scores = {'precision':[], 'recall':[], 'accuracy':[], 'f1':[]}

for train, test in KFold(dataset.data.shape[0], n_folds=12, shuffle=True):
        X_train, X_test = dataset.data[train], dataset.data[test]
        y_train, y_test = dataset.target[train], dataset.target[test]

        modeler.X = X_train
        modeler.y = y_train

        modeler.fit(model_list=['KNeighborsClassifier', 'RandomForestClassifier'])
        print("ran multifit")

        modeler.X_test = X_test
        predicted_df = modeler.predict(model_list=['KNeighborsClassifier', 'RandomForestClassifier'])
        print("ran predicted")

        expected  = y_test
        predicted = predicted_df['RandomForestClassifier']

        print(predicted.head())
        # Append our scores to the tracker
        #scores['precision'].append(metrics.precision_score(expected, predicted, average="weighted"))
        #scores['recall'].append(metrics.recall_score(expected, predicted, average="weighted"))
        #scores['accuracy'].append(metrics.accuracy_score(expected, predicted))
        #scores['f1'].append(metrics.f1_score(expected, predicted, average="weighted"))
