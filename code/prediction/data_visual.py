##Imports##

#import numpy as np
#import pandas as pd
#from scipy import stats, integrate
#import matplotlib.pyplot as plt
#import seaborn as sns
#sns.set(style="whitegrid", color_codes=True)
#np.random.seed(sum(map(ord, "categorical")))

from matplotlib import colors
from matplotlib.colors import ListedColormap
from bokeh.charts import BoxPlot, output_file, show
from sklearn.metrics import classification_report
import run_models
import sys

#################################
#Thanks Rebecca!
from matplotlib import colors
from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt
import numpy as np
def plot_classification_report(cr, title = None, cmap = None):

	#Make the District Data Labs heatmap the default
	if cmap is None:
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

	fig = plt.imshow(matrix, interpolation='nearest', cmap=cmap, vmin=0.5,vmax=1)
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

#def my_cool_graph(modeler):
  # modelar = classification_report(modeler.X_test,modeler.Y_test)
   #cr = modelar.answers
   #plot_classification_report(modelar)
#pass

#def roc_compare_two(y, yhats, models):
  #  f, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
 #   for yhat, m, ax in ((yhats[0], models[0], ax1), (yhats[1], models[1], ax2)):
  #  false_positive_rate, true_positive_rate, thresholds = roc_curve(y,yhat)
#	roc_auc = auc(false_positive_rate, true_positive_rate)
  #  ax.set_title('ROC for %s' % m)
  #  ax.plot(false_positive_rate, true_positive_rate, \
  #              c='#2B94E9', label='AUC = %0.2f'% roc_auc)
 #       ax.legend(loc='lower right')
  #      ax.plot([0,1],[0,1],'m--',c='#666666')
  #  plt.xlim([0,1])
  #  plt.ylim([0,1.1])
  #  plt.show()

#y_true_svc, y_pred_svc = get_preds(stdfeatures, labels, LinearSVC())
#y_true_knn, y_pred_knn = get_preds(stdfeatures, labels, KNeighborsClassifier())

#actuals = np.array([y_true_svc,y_true_knn])
#predictions = np.array([y_pred_svc,y_pred_knn])
#models = ['LinearSVC','KNeighborsClassifier']

if __name__ == '__main__':

    if len(sys.argv) > 1:
        pickle_name = sys.argv[1]
    else:
        pickle_name = 'modeler.pickle'

    modeler = run_models.load_modeler_pickle(pickle_name)

    y_pred = modeler.answers["RandomForest"]
    cr = classification_report( modeler.y_test, y_pred)
    plot_classification_report(cr)
