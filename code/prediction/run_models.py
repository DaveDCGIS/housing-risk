##################################################
#Imports
##################################################
import numpy as np
import pandas
import sklearn
from sklearn import metrics
from sklearn.model_selection import train_test_split

import pipeline

##################################################
#Load the data
##################################################
def load_sample_data():
    data = pandas.read_csv('./wine_data/wine.data', header=None)
    data.columns = ['Class'
                    , 'Alcohol'
                    , 'Malic acid'
                    , 'Ash'
                    , 'Alcalinity of ash'
                    , 'Magnesium'
                    , 'Total phenols'
                    , 'Flavanoids'
                    , 'Nonflavanoid phenols'
                    , 'Proanthocyanins'
                    , 'Color intensity'
                    , 'Hue'
                    , 'OD280/OD315 of diluted wines'
                    , 'Proline'
                    ]
    return data

def load_real_data():
    data = pipeline.get_decisions_table()
    return data

def run_models(data):
    data = pipeline.run_pipeline(data)
    print(data.head())

    X = data.iloc[:,1:].values
    y = data.iloc[:,0].values

    #Implement our pipeline
    print("--------starting pipeline---------")
    print(X[:,:5])
    pipe = pipeline.get_custom_pipeline()
    X_mod = pipe.fit_transform(X)
    print(X_mod[:,:5])

    #Just one split for now
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

    ##################################################
    #Set up our ManyModels instance
    ##################################################
    import risk_models
    modeler = risk_models.ManyModels()

    #Attach our unfitted model instances to the ManyModels instance
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.linear_model import LogisticRegression
    modeler.models = {"KNeighborsClassifier_6": sklearn.neighbors.KNeighborsClassifier(n_neighbors=6)
                      , "KNeighborsClassifier_12": sklearn.neighbors.KNeighborsClassifier(n_neighbors=12)
                      , "RandomForestClassifier": sklearn.ensemble.RandomForestClassifier()
                      , "LogisticRegression": sklearn.linear_model.LogisticRegression(penalty='l1', C=0.1)
                     }

    #Attach training data
    modeler.X = X_train
    modeler.y = y_train

    #We can call fit in 3 different ways depending on our needs.
    modeler.fit("KNeighborsClassifier_6")    #fit just one model
    modeler.fit(model_list=['KNeighborsClassifier_12', 'RandomForestClassifier'])   #fit a list of models
    modeler.fit() #fits all models

    #Attach testing data
    modeler.X_test = X_test
    modeler.y_test = y_test

    #run all models. This method also allows single entries or a list if desired
    predicted_df = modeler.predict()

    #If there is a y_test attached, the predict() method automatically calculates the scores
    #using PrettyPrinter because modeler.scores is a nested dictionary
    import pprint
    pp = pprint.PrettyPrinter()
    print("Model performance:")
    pp.pprint(modeler.scores)

    print(modeler.answers.head(20))

if __name__ == '__main__':
    data = load_real_data()
    print(data.head())
    run_models(data)
