##################################################
#Imports
##################################################
import numpy
import pandas
import sklearn
from sklearn import metrics
from sklearn.model_selection import train_test_split
import sys
import pickle
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
def load_real_data(debug = False):
    dataframe = data_utilities.get_decisions_table(equal_split = True)
    if debug == True:
        dataframe.to_csv('before.csv')
    return dataframe

def load_sample_data(debug = False):
    dataframe = data_utilities.get_sample_decisions_table(equal_split = True)
    if debug == True:
        dataframe.to_csv('before.csv')

    return dataframe

def load_data_pickle():
    logging.info("Loading from pickle...")
    with open('dataframe.pickle', 'rb') as f:
        return pickle.load(f)

def pickle_dataframe(dataframe):
    with open('dataframe.pickle', 'wb') as f:
        pickle.dump(dataframe, f)

def pickle_dataframe(dataframe):
    with open('dataframe.pickle', 'wb') as f:
        pickle.dump(dataframe, f)

def check_array_errors(array):
    '''
    Can be added to another function to do debugging of errors associated with array formatting before passing to sklearn models
    '''

    #Debugging for the NaN error
    finite_check = numpy.all(numpy.isfinite(array))
    nan_check = numpy.any(numpy.isnan(array))
    print("Finite: {}, NaN: {}".format(finite_check, nan_check))
    print('bad_indices, inf ', numpy.where(numpy.isinf(array)))
    print('bad_indices, nan ', numpy.where(numpy.isnan(array)))


def run_models(dataframe, debug = False):

    dataframe = data_utilities.clean_dataframe(dataframe, debug = debug)

    #Move the data into Numpy arrays - some pipeline methods require Numpy so cleaner to convert explicitly up front instead of passing in the dataframe
    logging.info("Splitting X and y from the data set...")
    col_names = list(dataframe)
    X = dataframe.iloc[:,1:].values
    y = dataframe.iloc[:,0].values
    X_names = col_names[1:]

    #Just one split for now
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=10)

    #Implement our pipeline
    pipe = data_utilities.get_custom_pipeline(col_names = X_names)
    logging.info("fit_transform our pipeline...")
    X_train = pipe.fit_transform(X_train)
    X_test = pipe.transform(X_test)

    #Save the transformed data to a CSV file if desired, to make sure our transformations are working properly
    if debug == True:
        numpy.savetxt("after_pipeline_train.csv", X_train, delimiter=",", fmt='%10.5f')


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
    modeler.y_names = data_utilities.get_meta_data()["categorical_features"]["decision"]

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

    #All of these argv are options you can pass to the command line to run certain parts of the file or change behavior of the program.
    #Typically there is not a need for any argv - calling the program plain will implement default behavior

    #Debug option is for outputting CSV files of the data for comparison purposes
    debug = True if 'debug' in sys.argv else False

    # Must use one of the below options to get the right data into the dataframe:
        # use_data_pickle
        # use_sample
        # use_real
    # Pickled data is an option to speed up running the program by not having to access the database every time.
    # Useful for debugging when you are running the program over and over again.
    if 'use_pickle' in sys.argv:
        dataframe = load_data_pickle()
    if 'use_sample' in sys.argv:
        dataframe = load_sample_data(debug=debug)
    if 'use_real' in sys.argv:
        dataframe = load_real_data(debug=debug)

    if 'make_data_pickle' in sys.argv:
        pickle_dataframe(dataframe)

    run_models(dataframe, debug = debug)
