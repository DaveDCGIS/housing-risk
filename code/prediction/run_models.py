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
    dataframe = data_utilities.get_decisions_table()
    if debug == True:
        dataframe.to_csv('before.csv')
    return dataframe

def load_sample_data(debug = False):
    dataframe = data_utilities.get_sample_decisions_table(equal_split = True)
    if debug == True:
        dataframe.to_csv('before_raw_sql_results.csv')

    return dataframe

def load_data_pickle():
    logging.info("Loading from pickle...")
    with open('dataframe.pickle', 'rb') as f:
        return pickle.load(f)

def load_modeler_pickle(pickle_name='modeler.pickle'):
    logging.info("Loading modeler from pickle...")
    with open(pickle_name, 'rb') as f:
        return pickle.load(f)

def pickle_dataframe(dataframe):
    with open('dataframe.pickle', 'wb') as f:
        pickle.dump(dataframe, f)

def pickle_modeler(modeler, filename):
    with open(filename, 'wb') as f:
        pickle.dump(modeler, f)

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


def run_models(dataframe, models_to_run = {}, debug = False, undersample=False):
    #A utility class that holds models, data, scores and pipeline
    modeler = data_utilities.ManyModels()

    #Basic data cleaning - mostly converting categorical variables to numbers and dealing with different Null formats in the source data.
    dataframe = data_utilities.clean_dataframe(dataframe, debug = debug)

    #Move the data into Numpy arrays
    logging.info("Splitting X and y from the data set...")
    col_names = list(dataframe)
    X = dataframe.iloc[:,1:].values
    y = dataframe.iloc[:,0].values
    X_names = col_names[1:]

    #Just one split for now
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=200, stratify = y)

    #Save the transformed data to a CSV file if desired, to make sure our transformations are working properly
    if debug == True:
        with open ("before_pipeline_training_data.csv", 'wb') as f:
            array_to_write = numpy.nan_to_num(X_train)
            print(array_to_write[:,:])
            numpy.savetxt(f, array_to_write, delimiter=",", fmt='%10.5f')

    #Implement our pipeline
    modeler.pipe = data_utilities.get_custom_pipeline(col_names = X_names)
    logging.info("fit_transform our pipeline...")
    X_train = modeler.pipe.fit_transform(X_train)
    X_test = modeler.pipe.transform(X_test)

    #Save the transformed data to a CSV file if desired, to make sure our transformations are working properly
    if debug == True:
        with open ("after_pipeline_training_data.csv", 'wb') as f:
            numpy.savetxt(f, X_train, delimiter=",", fmt='%10.5f')

    #under sample the 'in' decisions from just the training data
    if undersample == True:
        from imblearn.under_sampling import RandomUnderSampler
        rus = RandomUnderSampler()
        X_train, y_train = rus.fit_sample(X_train, y_train)


    ##################################################
    #Set up our models
    ##################################################
    #Attach our unfitted model instances to the ManyModels instance
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.linear_model import LogisticRegression
    from sklearn.naive_bayes import GaussianNB
    from sklearn.svm import SVC
    

    modeler.models = {    "KNeighbors_default": sklearn.neighbors.KNeighborsClassifier()
                      , "RandomForest": sklearn.ensemble.RandomForestClassifier()
                      , "LogisticRegression": sklearn.linear_model.LogisticRegression(penalty='l1', C=0.1)
                      , "GaussianNB": GaussianNB()
                      , "SVC_rbf": SVC(kernel = 'rbf', probability = True, random_state = 0)
                      , "SVC_linear": SVC(kernel = 'linear', probability = True,  random_state = 0)
                      , "SVC_poly": SVC(kernel = 'poly', degree = 3, probability = True,  random_state = 0)
                      }

    #Different method for KNeighbors allows us to compare multiple k's
    for i in range(3,13):
        modeler.models["KNeighbors_{}".format(i)] = sklearn.neighbors.KNeighborsClassifier(n_neighbors=i)

    #Attach training data
    modeler.X = X_train
    modeler.y = y_train
    modeler.y_names = data_utilities.get_meta_data()["categorical_features"]["decision"]

    #Convert our true/false dictionary into a list.
    #TODO would be good to add a dictionary of true/false as another way to pass models to run.
    model_list = []
    for key in models_to_run:
        if models_to_run[key] == True:
            model_list.append(key)
    logging.info("Running models: {}".format(str(model_list)))
    modeler.fit(model_list=model_list)


    #Do a quick PCA
    from sklearn.decomposition import PCA
    pca = PCA(n_components = 2, random_state=0) 
    pca.fit(X_train)
    pca_coefficients = pandas.DataFrame(pca.components_,index = ['PC-1','PC-2'])
    if debug==True:
        pca_coefficients.to_csv('pca_coefficients.csv')

    #Attach testing data and create predictions (also calculates scores)
    modeler.X_test = X_test
    modeler.y_test = y_test
    predicted_df = modeler.predict(model_list)

    return modeler

def predict_all_models(dataframe, modeler, debug=False):

    dataframe = data_utilities.clean_dataframe(dataframe, debug = debug)

    #Move the data into Numpy arrays
    col_names = list(dataframe)
    X = dataframe.iloc[:,:].values
    X_names = col_names[:]

    #Implement our pipeline
    logging.info("fit_transform our pipeline...")
    X = modeler.pipe.transform(X)

    #Attach testing data and create predictions
    modeler.y_test = None
    modeler.X_test = X
    predicted_df = modeler.predict()

    return modeler

def print_classification_reports(modeler, models_to_run = {}):
    logging.info("-"*45)
    logging.info("Model Performance:")
    logging.info("-"*45)
    for key in models_to_run:
        if models_to_run[key] == True:
            logging.info("{} Classification Report".format(key))
            logging.info(modeler.scores[key]['classification_report'])

if __name__ == '__main__':

    # Below are command line options. None are needed, except for a method for telling the run_models method
        #which models to run. Use argument --all to all, otherwise either edit the dictionary manually or pass each model name as an argument.

    #Debug option is for outputting CSV files of the data for checking that transformations are happining properly
    debug = True if 'debug' in sys.argv else False

    # Pickled data is an option to speed up running the program by not having to access the database every time.
    # Useful for debugging when you are running the program over and over again.
    if 'use_pickle' in sys.argv:
        dataframe = load_data_pickle()
    elif 'use_sample' in sys.argv:
        dataframe = load_sample_data(debug=debug)
    elif 'use_real' in sys.argv:
        dataframe = load_real_data(debug=debug)
    else:
        dataframe = load_real_data(debug=debug)


    if 'make_data_pickle' in sys.argv:
        pickle_dataframe(dataframe)

    #Use argument variables to decide which of our models to run this time. Each one can be passed as a separate argument variable, or use 'all' to run them all
    #Initialize with no models running
    models_to_run = {
        'KNeighbors_default': False,
        'RandomForest': False,
        'LogisticRegression': False,
        'GaussianNB': False,
        'SVC_rbf':False,
        'SVC_linear':False,
        'SVC_poly': False
    }

    #KNeighbors
    for i in range(3,13):
        models_to_run["KNeighbors_{}".format(i)] = False

    if '--all' in sys.argv:
        for key in models_to_run:
            models_to_run[key] = True
    for arg in sys.argv:
        if arg in models_to_run:
            models_to_run[arg] = True

    #Defaults for sampling method
    undersample = False
    if '--undersample' in sys.argv:
        undersample = True

    #Run the model. Edit these notes
    modeler = run_models(dataframe, models_to_run, debug = debug, undersample=undersample)
    modeler.version = "add_version_name_here"
    modeler.notes = "Add description of what was modeled"

    if 'make_modeler_pickle' in sys.argv:
        pickle_modeler(modeler, modeler.version + "_modeler.pickle")

    #logging.info("OneHot Encoded Variable specs")
    #How to interpret this data:
        # - integer i in feature_indices_list[i] indicates the first column index occupied by the categorical variable that was in position [i] in the source matrix.
        #   That column occupies all positions between position returned by [i] and one less than position returned by [i+1]
        #   But, not all of these are actually printed to the matrix (some are suppressed)
        # - Active features lists all features that are actually encoded in the matrix.
        # - n_features lists the number of features actually identified in each column (which should correspond to which ones have values suppressed)
        # Could use this logic to re-label the data.
        # onehotencoder returns the matrix with categorical values listed first and continuous values listed second (i.e. the order is rearranged from what is provided
    #logging.info("feature_indices_ from OneHotEncoder for each categorical feature: {}".format(modeler.pipe.named_steps['onehot'].feature_indices_))
    #logging.info("Active feature indices: {}".format(modeler.pipe.named_steps['onehot'].active_features_))
    #logging.info("n_values in each categorical feature: {}".format(modeler.pipe.named_steps['onehot'].n_values_))



    #temporary tests for current dev stuff:
    print_classification_reports(modeler, models_to_run)
