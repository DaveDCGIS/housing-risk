##################################################
#Imports
##################################################
#external Imports
import numpy as np
import pandas
import seaborn as sns
import matplotlib.pyplot as plt

#local imports
import data_utilities
import run_models

#Setup
sns.set(style="white", context="talk")
rs = np.random.RandomState(7)
f, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(8, 6), sharex=True)


#Get the data we want to graph
modeler = run_models.load_modeler_pickle()

#Extract the scores needed and reformat them into the groupings needed by the graph
scores_columns = ['model_name','precision_in','precision_out', 'recall_in', 'recall_out']
scores_array = np.empty((0,5))
i = 1
for key in modeler.scores:
    precision = modeler.scores[key]["precision"] #numpy array of two values for precision of each class
    recall = modeler.scores[key]["recall"] #numpy array of two values for recall of each class
    test_array = np.concatenate(([key],precision, recall), axis=0)
    reshaped_array = np.reshape(test_array, (1,5))
    print(type(reshaped_array[0,1]))
    scores_array = np.append(scores_array, reshaped_array, axis=0)
    i += 1





x = scores_array[:,0]
y1 = scores_array[:,1]
y2 = scores_array[:,2]
y3 = rs.choice(y1, 9, replace=False)
y4 = rs.choice(y1, 9, replace=False)

print(x,y1)
print(type(x[0]))

print(type(y1[0]))
#x = np.array(list("ABCDEFGHIJKLM"))
#y1 = np.arange(1, 13)
#y2 = scores_array[:,2]
#y3 = rs.choice(y1, 9, replace=False)
#y4 = rs.choice(y1, 9, replace=False)

#Palettes
#one method we could use
pal1 = sns.cubehelix_palette(x.size, start=0, rot=-0.5)
pal2 = sns.cubehelix_palette(x.size, start=1, rot=-0.5)
pal3 = sns.cubehelix_palette(x.size, start=2, rot=-0.5)
pal4 = sns.cubehelix_palette(x.size, start=2, rot=-0.5)

#overwrite above method
pal1 = "Reds"
pal2 = "Oranges"
pal3 = "Greens"
pal4 = "Blues"


sns.barplot(x, y1, palette=pal1, ax=ax1)
ax1.set_ylabel("Precision - In")

# Center the data to make it diverging
sns.barplot(x, y2, palette=pal2, ax=ax2)
ax2.set_ylabel("Recall - In")

# Randomly reorder the data to make it qualitative
sns.barplot(x, y3, palette=pal3, ax=ax3)
ax3.set_ylabel("Precision - Out")

sns.barplot(x, y4, palette=pal4, ax=ax4)
ax4.set_ylabel("Recall - Out")


# Finalize the plot
sns.despine(bottom=True)
plt.setp(f.axes, yticks=[])
plt.tight_layout(h_pad=3)


plt.savefig("output.png")
