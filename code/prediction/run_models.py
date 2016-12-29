##################################################
#Imports
##################################################
import numpy
import pandas
import sklearn
from sklearn import metrics
from sklearn.model_selection import train_test_split
import sys

#Configure logging. See /logs/example-logging.py for examples of how to use this.
import logging
logging_filename = "../logs/pipeline.log"
logging.basicConfig(filename=logging_filename, level=logging.DEBUG)
#Pushes everything from the logger to the command line output as well.
#logging.getLogger().addHandler(logging.StreamHandler())

import data_utilities

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

def load_real_data(debug = False):
    dataframe = data_utilities.get_decisions_table(equal_split = True)
    if debug == True:
        dataframe.to_csv('before.csv')

    return dataframe

def check_array_errors(array):

    #Debugging for the NaN error
    finite_check = numpy.all(numpy.isfinite(array))
    nan_check = numpy.any(numpy.isnan(array))
    print("Finite: {}, NaN: {}".format(finite_check, nan_check))
    print('bad_indices, inf ', numpy.where(numpy.isinf(array)))
    print('bad_indices, nan ', numpy.where(numpy.isnan(array)))


def run_models(dataframe, debug = False):
    dataframe = data_utilities.clean_dataframe(dataframe)

    #Move the data into Numpy arrays
    logging.info("Splitting X and y from the data set...")
    X = dataframe.iloc[:,1:].values
    y = dataframe.iloc[:,0].values

    #Implement our pipeline
    pipe = data_utilities.get_custom_pipeline()
    logging.info("fit_transform our pipeline...")
    X_mod = pipe.fit_transform(X)

    #Save the transformed data to a CSV file if desired, to make sure our transformations are working properly
    if debug == True:
        numpy.savetxt("after.csv", X_mod, delimiter=",", fmt='%10.5f')

    #Just one split for now
    X_train, X_test, y_train, y_test = train_test_split(X_mod, y, test_size=0.3, random_state=0)


    ##################################################
    #Set up our ManyModels instance
    ##################################################
    modeler = data_utilities.ManyModels()

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
    modeler.fit("RandomForestClassifier")    #fit just one model
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

    return modeler

if __name__ == '__main__':

    #Debug option is for outputting CSV files of the data for comparison purposes
    debug = False
    if 'debug' in sys.argv:
        debug = True

    dataframe = load_real_data(debug=debug)
    run_models(dataframe, debug = debug)
