
import logging
import psycopg2
import datetime
import time
import pandas as pd
import csv
from sqlalchemy import create_engine

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
	'db_connect_str': "dbname=temphousingrisk user=postgres password=postgres port=5433", #used with psycopg2.connect('')
	'engine_str': 'postgresql://postgres:postgres@localhost:5433/temphousingrisk', #used with create_engine() method
	'snapshots_csv_filename': 'snapshots_to_load_test.csv',
}

#sample code from http://initd.org/psycopg/docs/usage.html
def sample_add_to_database():
	# Connect to an existing database
	# Troubleshooting notes:
	#  1) Database must already be created
	#  2) Make sure the port matches your copy of the database - this is different per installation.
	#       Default is 5432, but if you have multiple Postgres installations it may be something else.
	#       Check your Postgres installation folder \PostgreSQL\9.5\data\postgresql.conf to find your port.
	#  3) user=postgres refers to the default install user, but the password=postgres is set manually during configuration.
	#     You can either edit your default user password, or add a new user. Note, setting the default user to NULL caused some problems for me.
	#  4) this function will throw an error the second time you run it because it will try to recreate a TABLE that already exists
	conn = psycopg2.connect(constants['db_connect_str'])

	# Open a cursor to perform database operations
	cur = conn.cursor()

	# Execute a command: this creates a new table
	cur.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")

	# Pass data to fill a query placeholders and let Psycopg perform
	# the correct conversion (no more SQL injections!)
	cur.execute("INSERT INTO test (num, data) VALUES (%s, %s)", (100, "abc'def"))

	# Query the database and obtain data as Python objects
	cur.execute("SELECT * FROM test;")
	print("Retreiving sample data from the database:")
	print(cur.fetchone())

	# Make the changes to the database persistent
	conn.commit()

	# Close communication with the database
	cur.close()
	conn.close()

def csv_to_sql(index_path):
	# Get the list of files to load - using Pandas dataframe (df), although we don't need most of the functionality that Pandas provides. #Example of how to access the filenames we will need to use: print(paths_df.get_value(0,'contracts_csv_filename'))
	paths_df = pd.read_csv(index_path, parse_dates=['date'])
	logging.info("Preparing to load " + str(len(paths_df.index)) + " files")

	# Connect to SQL - uses sqlalchemy so that we can write from pandas dataframe.
	engine = create_engine(constants['engine_str'])

	for index, row in paths_df.iterrows():
		full_path = row['path'] + row['filename']
		tablename = row['table_name']
		logging.info("loading table " + str(index + 1) + " (" + tablename + ")")
		contracts_df = pd.read_csv(full_path) # parse_dates=['tracs_effective_date','tracs_overall_expiration_date','tracs_current_expiration_date']
		logging.info("  in memory...")
		contracts_df.to_sql(tablename, engine, if_exists='replace')
		logging.info("  table loaded")


if __name__ == '__main__':
	#sample_add_to_database()
	csv_to_sql(constants['snapshots_csv_filename'])
