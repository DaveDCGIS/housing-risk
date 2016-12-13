##########################################################################
## Summary
##########################################################################
'''
tools for connecting to the database, which can be used in all of the project folders
'''

##########################################################################
## Imports & Configuration
##########################################################################
from sqlalchemy import create_engine
import json

constants = {
    'secrets_filename': '\secrets.json',
    'manifest_filename': '\snapshots_manifest.csv',
    'date_headers_filename': '\postgres_date_headers.json',
}

#Allow modules to import each other at parallel file structure (TODO clean up this configuration in a refactor)
from inspect import getsourcefile
import os.path
import sys
current_path = os.path.abspath(getsourcefile(lambda:0))
current_dir = os.path.dirname(current_path)
parent_dir = current_dir[:current_dir.rfind(os.path.sep)]
sys.path.insert(0, parent_dir)

##########################################################################
## Functions
##########################################################################
def get_connect_str(database_choice):
    "Loads the secrets json file to retrieve the connection string"
    with open(current_dir + constants['secrets_filename']) as fh:
        secrets = json.load(fh)
    return secrets[database_choice]['connect_str']
