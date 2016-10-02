
import logging
import psycopg2


#Configure logging. See /logs/example-logging.py for examples of how to use this.
logging_filename = "../logs/ingestion.log"
logging.basicConfig(filename=logging_filename, level=logging.DEBUG)
logging.warning("--------------------starting module------------------")


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
	conn = psycopg2.connect("dbname=temphousingrisk user=postgres password=postgres port=5433")

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






if __name__ == '__main__':
	sample_add_to_database()
	print("completed")




