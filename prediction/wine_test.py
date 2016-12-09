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
            , 'winetypes': "./wine_data/wine.data"
            , 'winetypes_readme': "./wine_data/wine.names"
    }

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
print(dataset['feature_names'])


##################################################
import sklearn
from sklearn import metrics
from sklearn.model_selection import train_test_split


import train_models
modeler = train_models.ManyModels()

#Attach our unfitted model instances to the modeler instance\
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression


modeler.models = {"KNeighborsClassifier_6": sklearn.neighbors.KNeighborsClassifier(n_neighbors=6)
                  , "KNeighborsClassifier_12": sklearn.neighbors.KNeighborsClassifier(n_neighbors=12)
                  , "RandomForestClassifier": sklearn.ensemble.RandomForestClassifier()
                  , "LogisticRegression": sklearn.linear_model.LogisticRegression(penalty='l1', C=0.1)
                 }


X_train, X_test, y_train, y_test = train_test_split(dataset.data, dataset.target, test_size=0.33, random_state=0)

######
#preprocessing
######
from sklearn.preprocessing import MinMaxScaler, StandardScaler
stdsc = StandardScaler()
X_train = stdsc.fit_transform(X_train)
X_test = stdsc.transform(X_test)


#Data is ready for modeling
modeler.X = X_train
modeler.y = y_train

#We can call fit in 3 different ways depending on our needs.
modeler.fit("KNeighborsClassifier_6") #fit just one model
modeler.fit(model_list=['KNeighborsClassifier_12', 'RandomForestClassifier']) #fit a list of models
modeler.fit() #fits all models

modeler.X_test = X_test
modeler.y_test = y_test

#run all models
predicted_df = modeler.predict()

import pprint
pp = pprint.PrettyPrinter()
pp.pprint(modeler.scores)



#print(predicted_df.head())
# Append our scores to the tracker
#scores['precision'].append(metrics.precision_score(expected, predicted, average="weighted"))
#scores['recall'].append(metrics.recall_score(expected, predicted, average="weighted"))
#scores['accuracy'].append(metrics.accuracy_score(expected, predicted))
#scores['f1'].append(metrics.f1_score(expected, predicted, average="weighted"))
