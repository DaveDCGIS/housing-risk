print("opening...")

import numpy, pandas


from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier

#Temporary method - initialize models we want to use
kn = KNeighborsClassifier(n_neighbors=12)
rf = RandomForestClassifier()


class ManyModels:
    def __init__(self):
        #dict of 'modelname':sklearn.model_instance
        #TODO - add method to establish these. Also, reset them if X or y are changed
        self.models = {   "KNeighborsClassifier": kn
                        , "RandomForestClassifier": rf
                      }

        self.X = numpy.array([[],[]]) #blank 2-d array
        self.y = numpy.array([]) #blank 1-d array
        self.answers = pandas.DataFrame() #Pandas dataframe where each row is a row of the test dataset, each column is a different model_list
        self.scores = pandas.DataFrame()

        self._X_test = None

    #Need to set the X_test data set universally, so that rows of self.answers will match
    def _setX_test(self, X_test=None):
        self._X_test = X_test
        #reset since rows will no longer match
        self.answers = pandas.DataFrame()
        self.scores = pandas.DataFrame()
    def _getX_test(self):
        return self._X_test
    X_test = property(_getX_test, _setX_test)

    def fit(self, model_list=None):

        model_list = self.clean_model_list(model_list)

        for key in model_list:
            self.models[key].fit(self.X, self.y)
            print("modeled")

        return self

    def predict(self, model_list=None):
        model_list = self.clean_model_list(model_list)

        for key in model_list:
            self.answers[key] = self.models[key].predict(self.X_test)

        return self.answers

    def clean_model_list(self, model_list):
            #Resolve defaults and turn a single string into a list
            if model_list == None:
                model_list = self.models.keys

            if isinstance(model_list, str):
                model_list = [model_list]

            if isinstance(model_list, list):
                return model_list
            else:
                raise ValueError('A provided model_list must be a list or a string.')
