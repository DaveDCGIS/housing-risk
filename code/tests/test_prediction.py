##########################################################################
## Prediction Package Tests
##########################################################################

# to execute tests, run from *project* root. This runs all test packages
# (this one and any other in the /tests folder)
#
#   nosetests --verbosity=2 --with-coverage --cover-inclusive --cover-erase tests
#
# for a list of available asserts:
# https://docs.python.org/2/library/unittest.html#assert-methods




##########################################################################
## Imports
##########################################################################

import unittest
from unittest import skip
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier

#Example import from our data structure
#from prediction.my_file import MyObjectName

##########################################################################
## Tests
##########################################################################

class PredictionTests(unittest.TestCase):

    def test_can_run_tests(self):
        """
        Make sure that nose tests works for test_prediction.py
        """
        assert(True)

    @skip('Test not written yet')
    def test_can_predict_risk(self):
        """
        Just an example of a test we might want to write.
        """
        pass


    @skip('Work in progress')
    def test_many_models_handles_reloading(self):
        import train_models
        modeler = train_models.ManyModels()
        dataset = Bunch('stuff') #need to get this to actually load a bunch of data

        X_train, X_test, y_train, y_test = train_test_split(dataset.data, dataset.target, test_size=0.33, random_state=1)
        modeler.X = X_train
        modeler.y = y_train

        #Attach our unfitted model instances to the modeler instance
        kn12 = KNeighborsClassifier(n_neighbors=12)
        kn6 = KNeighborsClassifier(n_neighbors=6)
        rf = RandomForestClassifier()
        modeler.models = {"KNeighborsClassifier_6": kn6
                          , "KNeighborsClassifier_12": kn12
                          , "RandomForestClassifier": rf
                         }

        #In another test, make sure all 3 methods work
        modeler.fit("KNeighborsClassifier_6") #fit just one model
        modeler.fit(model_list=['KNeighborsClassifier_12', 'RandomForestClassifier']) #fit a list of models
        modeler.fit() #fits all models

        modeler.X_test = X_test
        predicted_df = modeler.predict(model_list=['KNeighborsClassifier_12'])

        assert(modeler.answers.head()) #should have content
        modeler.X_test = X_test
        assert(modeler.answers.head()) #should be empty dataframe
        predicted_df = modeler.predict(model_list=['KNeighborsClassifier_6','KNeighborsClassifier_12', 'RandomForestClassifier'])
        assert(modeler.answers.head()) #should have content again
