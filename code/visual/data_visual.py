##Imports##

#import numpy as np
#import pandas as pd
#from scipy import stats, integrate
#import matplotlib.pyplot as plt
#import seaborn as sns
from bokeh.charts import BoxPlot, output_file, show
from 
#sns.set(style="whitegrid", color_codes=True)
#np.random.seed(sum(map(ord, "categorical")))

def make_cool_plot(modeler):
p= BoxPlot(values='modeler', label=['X','Y'])
output_file("boxplot.html")
show(p)

#predicted values for each model
answers_dataframe = modeler.answers

#'real' answers
y = modeler.y_test

#score data
kneighbors_accuracy = modeler.scores['KNeighborsClassifier_6'].accuracy
kneighbors_dictionary = modeler.scores['KNeighborsClassifier_6']

#iterate over a dictionary - this might be wrong syntax
for key, value in kneighbors_dictionary
	list_of_scores.append(value)
	print("Key: ".format(key))
	print("Value: ".format(value))
	










   
   
