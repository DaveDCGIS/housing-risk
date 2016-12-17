##########################################################################
## Summary
##########################################################################

'''
Creates flat table of decisions from our Postgres database and runs the prediction pipeline.
Starting point for running our models.
'''


##########################################################################
## Imports & Configuration
##########################################################################
import logging
import pandas as pd

#Configure logging. See /logs/example-logging.py for examples of how to use this.
logging_filename = "../logs/pipeline.log"
logging.basicConfig(filename=logging_filename, level=logging.DEBUG)
logging.warning("--------------------starting pipeline.py------------------")
#Pushes everything from the logger to the command line output as well.
logging.getLogger().addHandler(logging.StreamHandler())

#Allow modules to import each other at parallel file structure (TODO clean up this configuration in a refactor, it's messy...)
from inspect import getsourcefile
import os.path, sys
current_path = os.path.abspath(getsourcefile(lambda:0))
current_dir = os.path.dirname(current_path)
parent_dir = current_dir[:current_dir.rfind(os.path.sep)]
repo_dir = parent_dir[:parent_dir.rfind(os.path.sep)]
sys.path.insert(0, parent_dir)

import database_management

##########################################################################
## Functions
##########################################################################

def run_simple_query():
    #Connect to the database
    database_connection = database_management.get_database_connection('database')
    query_result = database_connection.execute("select snapshot_id, table_name from manifest where snapshot_id='c2005-07'")
    for query_row in query_result:
        print(query_row['snapshot_id'] + " | " + query_row['table_name'])

def get_decisions_table():
    #Connect to the database
    database_connection = database_management.get_database_connection('database')
    query_result = database_connection.execute("select snapshot_id, table_name from manifest where snapshot_id='c2005-07'")

    # Open and read the SQL command file as a single buffer
    query_path = parent_dir + "\wrangling\decisions_partial_churn_filter.sql"
    fd = open(query_path, 'r')
    sqlFile = fd.read()
    fd.close()
    query_text = "select * from (" + sqlFile +  """
                                ) as temp
                inner join contracts
                on contracts.contract_number = temp.contract_number
                where churn_flag<>'churn' and decision in ('in', 'out')
                """

    query_result = pd.read_sql(query_text, database_connection)
    print(query_result.head())
    return query_result

if __name__ == '__main__':
    #run_simple_query()
    decisions_df = get_decisions_table()
