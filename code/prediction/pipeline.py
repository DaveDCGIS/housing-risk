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
    query_text = "select" + """
                        temp.decision

                        /*, rent.hd01_vd01 as median_rent*/

                        /*, lag(c.contract_term_months_qty,1) over (partition by c.contract_number order by c.snapshot_id) term_mths_lag*/
                        , c.contract_term_months_qty
                        , c.assisted_units_count

                        , c.is_hud_administered_ind
                        , c.program_type_group_name

                        , c.rent_to_FMR_ratio
                        , c."0br_count" br0_count
                        , c."1br_count" br1_count
                        , c."2br_count" br2_count
                        , c."3br_count" br3_count
                        , c."4br_count" br4_count
                        , c."5plusbr_count" br5_count
                        """ + "from (" + sqlFile +  """
                                ) as temp
                inner join contracts as c
                on c.contract_number = temp.contract_number and c.snapshot_id = temp.snapshot_id
                inner join geocode as g
                on c.property_id = g.property_id
                inner join acs_rent_median as rent
                on g.geoid::text = rent.geo_id2::text

                where churn_flag<>'churn' and decision in ('in', 'out')
                """

    query_dataframe = pd.read_sql(query_text, database_connection)
    return query_dataframe
def get_custom_pipeline():

    from sklearn.preprocessing import StandardScaler, Imputer, LabelEncoder, MinMaxScaler, OneHotEncoder
    from sklearn.pipeline import Pipeline

    #TODO figure out how to use column names instead of numbers
    pipeline = Pipeline([('onehot', OneHotEncoder(categorical_features=[3], sparse=False))])

    return pipeline


def run_pipeline(dataframe):

    #categorical encoding - method #1
    decision_mapping = {'in': 1, 'out': 0}
    dataframe['decision'] = dataframe['decision'].map(decision_mapping)
    is_mapping = {'Y': 1, 'N': 0} #used for any field that starts with is_
    dataframe['is_hud_administered_ind'] = dataframe['is_hud_administered_ind'].map(is_mapping)

    #method #2
    from sklearn.preprocessing import LabelEncoder
    label_encoder_program_name = LabelEncoder()
    dataframe['program_type_group_name'] = label_encoder_program_name.fit_transform(dataframe['program_type_group_name'])

    #handle imputation
    pass

    #scaling
    #from sklearn.preprocessing import MinMaxScaler, StandardScaler
    #stdsc = StandardScaler()
    #dataframe = stdsc.fit_transform(dataframe)

    #TODO will change this to return a numpy array instead
    return dataframe



if __name__ == '__main__':
    dataframe = get_decisions_table()
    data_array = run_pipeline(dataframe)
