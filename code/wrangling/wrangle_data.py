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

#Database stuff
import database_management
import sqlalchemy

#############################
#FUNCTIONS
#############################
def run_simple_query():
    database_connection = database_management.get_database_connection('database')
    query_result = database_connection.execute("select snapshot_id, table_name from manifest where snapshot_id='c2005-07'")
    for query_row in query_result:
        print(query_row['snapshot_id'] + " | " + query_row['table_name'])


def drop_table(tablename):
    session = database_management.get_database_session('database')
    try:
        query_result = session.execute("drop table {}".format(tablename))
        session.commit()
        logging.info("table dropped: {}".format(tablename))
    except sqlalchemy.exc.ProgrammingError:
        logging.info("table not found: {}".format(tablename))
    session.close()

def make_table(sqlfilename,add_create_statement=False, table_name=None):

    session = database_management.get_database_session('database')

    # Open and read the file as a single buffer
    #fd = open('sample.sql', 'r')
    fd = open(sqlfilename, 'r')
    sqlFile = fd.read()
    fd.close()

    if add_create_statement == True:
        sqlQuery = "CREATE TABLE {} AS (".format(table_name) + sqlFile + ")"
    else:
        sqlQuery = sqlFile

    query_result = session.execute(sqlQuery)
    logging.info("Table created: {}".format(sqlfilename))
    session.commit()
    session.close()

if __name__ == '__main__':

    if 'drop' in sys.argv:
        drop_decisions()
    if 'rebuild' in sys.argv:
        drop_table('decisions_tests')
        drop_table('decisions')
        make_table('make_decisions_tests.sql')
        make_table('decisions_table_only.sql',True,'decisions')
