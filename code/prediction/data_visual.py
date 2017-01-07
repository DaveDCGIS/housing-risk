##Imports##

#import numpy as np
#import pandas as pd
#from scipy import stats, integrate
#import matplotlib.pyplot as plt
#import seaborn as sns
#sns.set(style="whitegrid", color_codes=True)
#np.random.seed(sum(map(ord, "categorical")))
from bokeh.charts import BoxPlot, output_file, show

import run_models

def demo_reading_from_modeler(modeler):
	#predicted values for each model
	answers_dataframe = modeler.answers
	y_pred = answers_dataframe["KNeighborsClassifier_6"]

	#'real' answers
	y_true = modeler.y_test

	#score data
	kneighbors_accuracy = modeler.scores['KNeighborsClassifier_6']['accuracy']
	kneighbors_dictionary = modeler.scores['KNeighborsClassifier_6']
	#not implemented:
	#kneighbors_classification_report = modeler.scores['KNeighborsClassifier_6']['classification_report']

	#print(modeler.scores)
	#print(modeler.answers.head())
	#print(type(modeler))
	#print(type(modeler.answers))

	#iterate over a dictionary - this might be wrong syntax
	list_of_scores = []
	for key in kneighbors_dictionary:
		list_of_scores.append(kneighbors_dictionary[key])
		print("Key: {}".format(key))
		print("Value: {}".format(kneighbors_dictionary[key]))

#################################
#Thanks Rebecca!
from matplotlib import colors
from matplotlib.colors import ListedColormap

def plot_classification_report(cr, title = None, cmap=None):

	#Make the District Data Labs heatmap the default
	if cmap is none:
		ddl_heat = ['#DBDBDB','#DCD5CC','#DCCEBE','#DDC8AF','#DEC2A0','#DEBB91',\
			            '#DFB583','#DFAE74','#E0A865','#E1A256','#E19B48','#E29539']
		cmap = colors.ListedColormap(ddl_heat)

	title = title or 'Classification report'
	lines = cr.split('\n')
	classes = []
	matrix = []

	for line in lines[2:(len(lines)-3)]:
	    s = line.split()
	    classes.append(s[0])
	    value = [float(x) for x in s[1: len(s) - 1]]
	    matrix.append(value)

	fig, ax = plt.subplots(1)

	for column in range(len(matrix)+1):
	    for row in range(len(classes)):
	        txt = matrix[row][column]
	        ax.text(column,row,matrix[row][column],va='center',ha='center')

	fig = plt.imshow(matrix, interpolation='nearest', cmap=cmap)
	plt.title(title)
	plt.colorbar()
	x_tick_marks = np.arange(len(classes)+1)
	y_tick_marks = np.arange(len(classes))
	plt.xticks(x_tick_marks, ['precision', 'recall', 'f1-score'], rotation=45)
	plt.yticks(y_tick_marks, classes)
	plt.ylabel('Classes')
	plt.xlabel('Measures')
	plt.show()
#end of DDL copied stuff
################################3

def my_cool_graph(modeler):
	#add your code here to make a graph by accessing the data contained in modeler
	pass

def roc_plot(modeler):
	#add your code here to make a graph by accessing the data contained in modeler
	pass


if __name__ == '__main__':
	dataframe = run_models.load_data_pickle()
	#dataframe = run_models.load_sample_data()
	modeler = run_models.run_models(dataframe)

	demo_reading_from_modeler(modeler)

	roc_plot(modeler)

	#this one is not tested yet:
	#plot_classification_report(modeler.scores["classification_report"])

	print("Imported succesfully!")
