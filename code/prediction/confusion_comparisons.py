##################################################
#Imports
##################################################
#external Imports
import numpy as np
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

for key in modeler.scores:
    #TODO - need to extract the right value from this classification_report and save them to numpy arrays as with the below example.
    #TODO - find out how classification_report is stored - can we access each number individually?
    print(modeler.scores[key]["classification_report"])
    
x = np.array(list("ABCDEFGHI"))
y1 = np.arange(1, 10)
y2 = y1 - 5
y3 = rs.choice(y1, 9, replace=False)
y4 = rs.choice(y1, 9, replace=False)

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
