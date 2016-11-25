
import numpy, pandas


class ManyModels:
    def __init__(self):
        self.models = {}            #dict of 'modelname':sklearn.model_instance
        self.X = np.array([[],[]]) #blank 2-d array
        self.y = np.array([]) #blank 1-d array
        self.answers = pandas.DataFrame() #Pandas dataframe with each row is a row of the test dataset, each column is a different model_list
        self.scores = pandas.DataFrame()

    def fit(self, model_list=None):

        model_list = clean_model_list(model_list)

        for key in model_list:
            self.models[key].fit(self.X)
            pass

        return self

    def predict(self, model_list=None, test_answers = None):
        model_list = clean_model_list(model_list)

        for key in model_list:
            self.answers[key] = self.models[key].predict(self.X)
            if test_answers != None
                self.scores[key] = average(test_answers - self.answers[key]) #compare answers to each other. TODO replace with r2 score or somesuch


    def clean_model_list(model_list):
            #Resolve defaults and turn a single string into a list
            if model_list = None:
                model_list = self.models.keys

            if isinstance(model_list, str):
                model_list = [model_list]

            if isinstance(model_list, list):
                return model_list
            else
                raise ValueError('A provided model_list must be a list or a string.')
