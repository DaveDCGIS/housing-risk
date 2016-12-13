##########################################################################
## Imports & Configuration
##########################################################################
import logging
#Configure logging. See /logs/example-logging.py for examples of how to use this.
logging_filename = "../logs/wrangling.log"
logging.basicConfig(filename=logging_filename, level=logging.DEBUG)
logging.warning("--------------------starting module------------------")
#Pushes everything from the logger to the command line output as well.
logging.getLogger().addHandler(logging.StreamHandler())

#Allow modules to import each other at parallel file structure (TODO clean up this configuration in a refactor)
from inspect import getsourcefile
import os.path
import sys
current_path = os.path.abspath(getsourcefile(lambda:0))
current_dir = os.path.dirname(current_path)
parent_dir = current_dir[:current_dir.rfind(os.path.sep)]
sys.path.insert(0, parent_dir)

#from ingestion import update_database
import database_management

#############################
#FUNCTIONS
#############################
connection_string = database_management.get_connect_str('database')
print(connection_string)
