import pickle
import data_utilities


modeler_name = "completed_models\\for_presentation_under_sampling_modeler.pickle"
fitted_model_file = "completed_models\\random_forest.pickle"
pipe_file = "completed_models\\pipe.pickle"

with open(modeler_name, 'rb') as f:
    modeler = pickle.load(f)


fitted_model = modeler.models['RandomForest']
pipe = modeler.pipe

with open(fitted_model_file, 'wb') as f:
    pickle.dump(fitted_model, f)
with open(pipe_file, 'wb') as f:
	pickle.dump(pipe, f)
	

print("Fitted model saved!")