##########################################################################
## Summary
##########################################################################

'''
Loads our flat file data into the Postgres database
'''


##########################################################################
## Imports & Configuration
##########################################################################
import logging
import json
import pandas as pd
from sqlalchemy import create_engine
import csv

#Configure logging. See /logs/example-logging.py for examples of how to use this.
logging_filename = "../logs/ingestion.log"
logging.basicConfig(filename=logging_filename, level=logging.DEBUG)
logging.warning("--------------------starting module------------------")
#Pushes everything from the logger to the command line output as well.
logging.getLogger().addHandler(logging.StreamHandler())

#############################
#CONSTANTS
#############################
constants = {
    'secrets_filename': 'secrets.json',
    'manifest_filename': 'temp_snapshots_test.csv',
    'date_headers_filename': 'postgres_date_headers.json',
}

def get_connect_str():
    "Loads the secrets json file to retrieve the connection string"
    logging.info("Loading secrets from {}".format(constants['secrets_filename']))
    with open(constants['secrets_filename']) as fh:
        secrets = json.load(fh)
    return secrets['database']['connect_str']

def get_column_names(path):
    with open(path) as f:
        myreader=csv.reader(f,delimiter=',')
        headers = next(myreader)
    return headers

def csv_to_sql(index_path):
    # Get the list of files to load - using Pandas dataframe (df)
    paths_df = pd.read_csv(index_path, parse_dates=['date'])
    logging.info("Preparing to load " + str(len(paths_df.index)) + " files")

    # Connect to SQL - uses sqlalchemy so that we can write from pandas dataframe.
    connect_str = get_connect_str()
    engine = create_engine(connect_str)

    for index, row in paths_df.iterrows():
        full_path = row['path'] + row['filename']
        tablename = row['table_name']

        logging.info("loading table " + str(index + 1) + " (" + tablename + ")")

        #Since different files have different date columns, we need to compare to the master list.
        headers = list(get_column_names(full_path))
        with open(constants['date_headers_filename']) as fh:
            date_headers = json.load(fh)
            parseable_headers = date_headers['date_headers']
        to_parse = list(set(parseable_headers) & set(headers))
        logging.info("  identified date columns: " + str(to_parse))

        csv_df = pd.read_csv(full_path, encoding="latin1", parse_dates=to_parse) #If we have null dates that are non-blank (coded nulls), need to use this: date_parser=parser #parser = lambda x: pd.to_datetime(x, format='%m/%d/%Y', errors='coerce')
        logging.info("  in memory...")

        #Add a column so that we can put all the snapshots in the same table
        csv_df['snapshot_id'] = row['snapshot_id']
        csv_df.to_sql(tablename, engine, if_exists='append')
        logging.info("  table loaded")

def access_to_sql():
    '''
    Currently not working - can't get driver...
    '''
    import pyodbc
    DBfile = "../data/section8/contracts_database/main-website/MF_Assistance_&_Sec8_Contracts_2016-08-02.mdb"
    conn = pyodbc.connect('DRIVER={Microsoft Access Driver (*.mdb)};DBQ='+DBfile)
    #or try this below if using with Access 2007, 2010 .accdb file
    #conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ='+DBfile)
    cursor = conn.cursor()

if __name__ == '__main__':
    #sample_add_to_database()
    csv_to_sql(constants['manifest_filename'])
    #access_to_sql()
