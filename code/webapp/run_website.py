##########################################################################
## Summary
##########################################################################
'''
Runs a Flask-based web server that can dynamically run our models for us.



Warning - overall pretty quick and dirty - not great attention payed to consistent
or short variable names, or the ability to reuse code sections. 
Just getting a website up in time for the presentation.


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
        print("No rent data replacement needed")
        #Probably the median_rent column already had all numbers in it
        pass

    return dataframe




##########################################################################
## Modeling setup and functions
##########################################################################
def predict(dataframe, model):
    new_dataframe = dataframe.copy()
    new_dataframe = clean_dataframe(new_dataframe, debug = False)
    X = new_dataframe.iloc[:,:].values
    X = pipe.transform(X)

    #Initial predictions
    y = model.predict(X)

    return y


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

only_identifying_fields_dataframe = dc_data.loc[:,['decision_data_year', 'altered_decision_data_year', 'rent_snapshot_id',
                                   'contract_snapshot_id', 'contract_number', 'property_name_text',
                                   'owner_organization_name', 'address', 'city', 'state', 'geoid',
                                   'geo_id2']]

##########################################################################
## Web Application
##########################################################################
app = Flask(__name__)
app.config['SECRET_KEY'] = 'ALIEXOPADPQLXSDIEOLQPPPOIM' #random string configured for demo purposes (would need to be config variable in a live site)



#form data
form = ['contract_term_months_qty', 'median_rent']

from flask.ext.wtf import Form
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import Required, NumberRange, Optional

class ModelParametersForm(Form):
    median_rent = IntegerField('Neighborhood median rent:', validators=[Optional(), NumberRange(500,3000)])
    contract_term_months_qty = IntegerField('Most recent contract duration (months):', validators=[Optional(), NumberRange(6,240)])
    submit = SubmitField('Create Predictions')



#views
@app.route('/', methods = ['GET', 'POST'])
def index():

    #Handle form configuration and setup
    model_parameters_form = ModelParametersForm()
    rent_entered = None
    months_entered = None


    if model_parameters_form.validate_on_submit():
        print("successful form validation")
        rent_entered = model_parameters_form.median_rent.data
        months_entered = model_parameters_form.contract_term_months_qty.data

    #Use the provided inputs to alter the modeling data
    data_copy = only_testing_fields_dataframe.copy()

    initial_y = predict(data_copy, random_forest)
    new_y = predict(data_copy, random_forest)




    if rent_entered != None or months_entered != None:
        if rent_entered != None:
            pass
            data_copy['median_rent'] = rent_entered
        if months_entered != None:
            pass
            #Assume that the current contract becomes the previous one, and then use the value entered
            data_copy['previous_contract_term_months'] = only_testing_fields_dataframe['contract_term_months_qty']
            data_copy['contract_term_months_qty'] = months_entered

    new_y = predict(data_copy, random_forest)

    #Quick validation for debugging
    count_out_decisions = 0
    for d in numpy.nditer(new_y):
        count_out_decisions = count_out_decisions + d
    print("Quantity of out decisions: {}".format(count_out_decisions))

    #Prep variables for display based on user inputs
    if rent_entered == None:
        rent_entered = "No changes"
    if months_entered == None:
        months_entered = "No changes"

    #Prep the list of buildings with their decision in format useful for the view page. 
    dc_contracts = [] #a list of dictionaries
    names_list = list(dc_data["property_name_text"])

    for index, value in enumerate(names_list):
        i = "in" if initial_y.item(index)==0 else 'out'
        n = "in" if new_y.item(index)==0 else 'out'
        new_building = {"property_name_text": value
                        ,"original_decision": i
                        ,"new_decision": n
                        }

        dc_contracts.append(new_building)

    return render_template('main.html', 
                            myvar = "dummy", 
                            dc_contracts = dc_contracts, 
                            model_parameters_form = model_parameters_form, 
                            rent_entered = rent_entered,
                            months_entered = months_entered
                            )


#Run the app
if __name__ == '__main__':
    app.run(debug=True)


