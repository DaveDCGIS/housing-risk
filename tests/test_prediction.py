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