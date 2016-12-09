print("importing train_models...")

import numpy, pandas
from sklearn import metrics

class ManyModels:
    '''
    A wrapper class for training multiple sklearn models on a single dataset
    The wrapper contains:
        -The models themselves (fitted or not), passed as a dictionary from the calling function
        -X and y arrays of training data.
        -an X_test set of testing data
        -The predicted answers of all models, stored as a dataframe with rows matching the X_test dataset

    Not optimized for memory use - instead it is designed for as much flexibility and access to source data,
    models, and prediction performance as possible for use in a learning context.
    '''

    def __init__(self):

        self.models = {}  #dict of 'modelname':sklearn.model_instance
        self.X = numpy.array([[],[]]) #blank 2-d array
        self.y = numpy.array([]) #blank 1-d array
        self.answers = pandas.DataFrame() #Pandas dataframe where each row is a row of the test dataset, each column is a different model_list
        self.scores = {} #Nested dictionary of shape {'modelname': {'precision': #, 'recall': #, 'accuracy': #, 'f1': # }}

        self.X_test = None
        self.y_test = None

    #@property lets us add additional logic to the getters and setters for the X_test property (e.g., resetting the answers and scores)
    @property
    def X_test(self):
        return self.__X_test
    @X_test.setter
    def X_test(self, X_test=None):
        self.__X_test = X_test
        #reset since rows will no longer match
        self.answers = pandas.DataFrame()
        self.scores = {}

    @property
    def y_test(self):
        return self.__y_test
    @y_test.setter
    def y_test(self, y_test=None):
        self.__y_test = y_test
        #reset since rows will no longer match
        self.answers = pandas.DataFrame()
        self.scores = {}

    def fit(self, model_list=None):
        model_list = self.clean_model_list(model_list)

        for key in model_list:
            self.models[key].fit(self.X, self.y)
            print("  fitted model: " + key)

        return self

    def predict(self, model_list=None):
        model_list = self.clean_model_list(model_list)

        for key in model_list:
            self.answers[key] = self.models[key].predict(self.X_test)

            self.scores[key] = { }
            if self.y_test is not None:
                self.scores[key]['precision'] = metrics.precision_score(y_true = self.y_test, y_pred = self.answers[key].as_matrix(), average="weighted")
                self.scores[key]['recall'] = metrics.recall_score(y_true = self.y_test, y_pred=self.answers[key], average="weighted")
                self.scores[key]['accuracy'] = metrics.accuracy_score(y_true = self.y_test, y_pred=self.answers[key])
                self.scores[key]['f1'] = metrics.f1_score(y_true = self.y_test, y_pred=self.answers[key], average="weighted")

        return self.answers

    def clean_model_list(self, model_list):
            #Resolve defaults and turn a single string into a list
            if model_list is None:
                model_list = list(self.models.keys())

            if isinstance(model_list, str):
                model_list = [model_list]

            if isinstance(model_list, list):
                return model_list
            else:
                raise ValueError('A provided model_list must be a list or a string.')
