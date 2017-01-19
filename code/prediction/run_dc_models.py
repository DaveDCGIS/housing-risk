

import run_models
import pickle
import pandas

def get_dc_decisions_table():

    database_connection = run_models.data_utilities.database_management.get_database_connection('database')
    query_path = "select_dc_buildings.sql"
    file = open(query_path, 'r')
    query_text = file.read()
    file.close()

    query_dataframe = run_models.pandas.read_sql(query_text, database_connection)

    return query_dataframe


def predict_dc_models(dataframe):

    only_testing_fields_dataframe = dataframe[['median_rent', 'contract_term_months_qty',
                               'previous_contract_term_months', 'assisted_units_count',
                               'rent_to_fmr_ratio', 'br0_count', 'br1_count', 'br2_count', 'br3_count',
                               'br4_count', 'br5_count', 'program_type_group_name',
                               'is_hud_administered_ind', 'is_acc_old_ind',
                               'is_acc_performance_based_ind', 'is_hud_owned_ind',
                               'owner_company_type', 'mgmt_agent_company_type',
                               'primary_financing_type']]


    filename = "completed_models\\for_presentation_under_sampling_modeler.pickle"

    with open(filename, 'rb') as f:
        modeler = pickle.load(f)


    updated_modeler = run_models.predict_all_models(only_testing_fields_dataframe, modeler, debug=False)
    print(updated_modeler.answers.head())

    return updated_modeler
if __name__ == '__main__':
    dataframe = get_dc_decisions_table()
    only_identifying_fields = dataframe[['decision_data_year', 'altered_decision_data_year', 'rent_snapshot_id',
       'contract_snapshot_id', 'contract_number', 'property_name_text',
       'owner_organization_name', 'address', 'city', 'state', 'geoid',
       'geo_id2']]

    updated_modeler = predict_dc_models(dataframe)

    predicted_answers = updated_modeler.answers
    rejoined_dataframe = pandas.concat([only_identifying_fields, predicted_answers], axis=1)
    simple_dataframe_predictions = rejoined_dataframe[['contract_number','property_name_text','RandomForest']]

    simple_dataframe_predictions.to_csv('predicted_dc_answers.csv')
