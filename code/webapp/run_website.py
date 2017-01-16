##########################################################################
## Summary
##########################################################################
'''
Runs a Flask-based web server that can dynamically run our models for us.
'''



##########################################################################
## Imports & Configuration
##########################################################################
from flask import Flask
from flask import render_template
import pickle
import pandas



#Allow modules to import each other at parallel file structure (TODO clean up this configuration in a refactor, it's messy...)
from inspect import getsourcefile
import os, sys, json
current_path = os.path.abspath(getsourcefile(lambda:0))
current_dir = os.path.dirname(current_path)
parent_dir = current_dir[:current_dir.rfind(os.path.sep)]
repo_dir = parent_dir[:parent_dir.rfind(os.path.sep)]
sys.path.insert(0, parent_dir)

#my imported modules somehow break the debug mode of Flask...
#import database_management
#import prediction.data_utilities as data_utilities
#data_utilities.test_import()


##########################################################################
## Application
##########################################################################

app = Flask(__name__)

#TODO currently not loading with no module named data_utilities error (although data_utilities is loading above). Google pickle problems load from different folder
#print("Loading modeler from pickle...")
#with open('modeler.pickle', 'rb') as f:
#    modeler = pickle.load(f)

#load data

#TODO stuff that needs to happen for proper data loading:
'''
* add back in the contract data, address data etc. to the query
* replace previous_contract_term_months (not available except for calculated decisions.... or could refactor decisions query)
* split the data between identifiers and model data

Current list of modeling fields (TODO this is to be updated):
    median_rent
    contract_term_months_qty
    previous_contract_term_months
    assisted_units_count
    is_hud_administered_ind
    program_type_group_name
    rent_to_fmr_ratio
    is_acc_old_ind
    is_acc_performance_based_ind
    rent_to_fmr_ratio
    br0_count
    br1_count
    br2_count
    br3_count
    br4_count
    br5_count
    is_hud_owned_ind
    owner_company_type
    mgmt_agent_company_type

Current list of identifier fields:
    decision_data_year
    altered_decision_data_year
    rent_snapshot_id
    contract_snapshot_id
    contract_number
    property_name_text
    owner_organization_name
    address
    city
    state
    geoid
    geo_id2

'''

dc_data = pandas.read_csv('static/example.csv')
print("Looaded csv of the dc_data")

#views
@app.route('/')
def index():

    dc_contracts = [] #a list of dictionaries, each dictionary is a data type.
    #Temporary method - convert the list of properties to a dictionary and randomly assign
    names_list = list(dc_data["property_name_text"])

    for value in names_list:
        new_building = {"property_name_text": value
                        ,"original_decision": 'in'
                        }
        if value in ['BEECHER COOPERATIVE          *                    ']:
            new_building["decision"] = "out"
        else:
            new_building["decision"] = "in"

        dc_contracts.append(new_building)

    return render_template('main.html', myvar = "dummy", dc_contracts = dc_contracts)


#Run the app
if __name__ == '__main__':
    app.run(debug=True)







    #print("App running...")
