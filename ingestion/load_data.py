
import logging
import pandas as pd

#Configure logging. See /logs/example-logging.py for examples of how to use this.
logging_filename = "../logs/ingestion.log"
logging.basicConfig(filename=logging_filename, level=logging.DEBUG)
logging.warning("--------------------starting module------------------")


##########################
#Classes to hold and manipulate our data
##########################

#Container for a single copy of the sec8contracts database from HUD. Contains both database tables (as pandas dataframes) plus dates.
class Sec8Snapshot(object):
	
	#All properties can be passed on initizalization; but, they can also be set later in the code if needed for clarity (hence the 'None' defaults)
	def __init__(self, contracts_df = None, properties_df = None, date=None, source=''):
		self.contracts_df = contracts_df     	#a Pandas dataframe with the 'contracts' table
		self.properties_df = properties_df		#a Pandas dataframe with the 'properties' table
		self.date = date 						#the date the snapshot was published
		self.source = source					#string representing where the copy came from, e.g. from HUD or from the Internet Archive


#Contains a list of multiple snapshots, as well as methods for comparing the snapshots
class Sec8Timeline(object):

	def __init__(self):
		#A list of Pandas dataframe objects, each representing a copy of the contracts table at a certain time
		self.snapshots = []

	def add(self,snapshot):
		self.snapshots.append(snapshot)
		#TODO do we want to sort the snapshots by their date stamp?

	def remove(self,snapshot):
		self.snapshots.remove(snapshot)

#database snapshots to be loaded
#A dictionary of dictionaries. TODO could convert the second dictionary to a named tuple to be a little cleaner.
#TODO - need to change the dates here to be actual date objects
sec8_flatfile_paths = {
	'current': {'date':'2016-08-02','contracts': "data\section8\contracts_database\main-website\sec8contracts_2016-08-02.csv", 'properties': ''},
	'2015': {'date':'2015-09-05','contracts': "data\section8\contracts_database\internetArchive\sec8contracts_2015-09-05.csv", 'properties': ''},
	'2011': {'date':'2011-09-22','contracts': "data\section8\contracts_database\internetArchive\sec8contracts_2011-09-22.csv", 'properties': ''},
}

def load_sec8_contracts(paths):
	timeline = Sec8Timeline()

	#TODO need to add properties paths and test their addition also
	for key in paths:
		contracts_df = pd.read_csv(paths[key]['contracts'], parse_dates=['tracs_effective_date','tracs_overall_expiration_date','tracs_current_expiration_date'])
		#properties_df = pd.read_csv(paths[key]['contracts'], parse_dates=['ownership_effective_date'])
		properties_df = None
		date = paths[key]['date']
		snapshot = Sec8Snapshot(contracts_df,properties_df,date)

		timeline.add(snapshot)

	return timeline

sec8_timeline = load_sec8_contracts(sec8_flatfile_paths)
print("Timeline made")
logging.info("finished timeline")
print(sec8_timeline)
print(len(sec8_timeline.snapshots))