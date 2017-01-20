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
import json
from sklearn.ensemble import RandomForestClassifier
import numpy

from sklearn.preprocessing import StandardScaler, Imputer, LabelEncoder, MinMaxScaler, OneHotEncoder
from sklearn.pipeline import Pipeline


def clean_dataframe(dataframe, debug=False):
    '''
    A modified version of clean_dataframe copied from the 
    prediction/data_utilities.py, edited so that it can operate 
    standalone (had conflicts with Flask)
    '''
    #Convert all the categorical names to numbers.
    with open('meta.json', 'r') as f:
            meta = json.load(f)

    categorical_features = meta['categorical_features']
    for column_name in categorical_features:
        if column_name in dataframe.columns:
            categories = categorical_features[column_name]
            categories_map = {x:i for i,x in enumerate(categories)}
            dataframe[column_name] = dataframe[column_name].map(categories_map)

    #Replacing string values in rent
    replace_mapping = { 'median_rent': {'-': numpy.nan,'100-': 100, '2,000+': 2000}}
    try:
        dataframe.replace(to_replace=replace_mapping, inplace=True)
        dataframe['median_rent'] = pandas.to_numeric(dataframe['median_rent'], errors='ignore')
    except TypeError:
        print("error caught")
        #Probably the median_rent column already had all numbers in it
        pass

    return dataframe




##########################################################################
## Modeling setup and functions
##########################################################################


#Get our data and models
with open('random_forest.pickle', 'rb') as f:
    random_forest = pickle.load(f)
with open('pipe.pickle', 'rb') as f:
    pipe = pickle.load(f)
dc_data = pandas.read_csv('static/dc_testing_data.csv')

#Split and clean our data
only_testing_fields_dataframe = dc_data.loc[:,['median_rent', 'contract_term_months_qty',
                               'previous_contract_term_months', 'assisted_units_count',
                               'rent_to_fmr_ratio', 'br0_count', 'br1_count', 'br2_count', 'br3_count',
                               'br4_count', 'br5_count', 'program_type_group_name',
                               'is_hud_administered_ind', 'is_acc_old_ind',
                               'is_acc_performance_based_ind', 'is_hud_owned_ind',
                               'owner_company_type', 'mgmt_agent_company_type',
                               'primary_financing_type']]

only_identifying_fields = dc_data[['decision_data_year', 'altered_decision_data_year', 'rent_snapshot_id',
       'contract_snapshot_id', 'contract_number', 'property_name_text',
       'owner_organization_name', 'address', 'city', 'state', 'geoid',
       'geo_id2']]
only_testing_fields_dataframe = clean_dataframe(only_testing_fields_dataframe, debug = False)
X = only_testing_fields_dataframe.iloc[:,:].values
X = pipe.transform(X)

#Initial predictions
y = random_forest.predict(X)
print(y)


##########################################################################
## Web Application
##########################################################################
app = Flask(__name__)


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


