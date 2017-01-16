##################################################
#Imports
##################################################
#system imports
import sys

#external Imports
import numpy as np
import pandas
import seaborn as sns
import matplotlib.pyplot as plt

#local imports
import data_utilities
import run_models



def reformat_scores(modeler):
    #Extract the scores needed and reformat them into the groupings needed by the graph
    scores_df = pandas.DataFrame(columns=['precision_in','precision_out', 'recall_in', 'recall_out'])
    for key in modeler.scores:
        precision = modeler.scores[key]["precision"] #numpy array of two values for precision of each class
        recall = modeler.scores[key]["recall"] #numpy array of two values for recall of each class
        all_scores = np.concatenate((precision,recall),axis=0)
        all_scores_inverted = np.reshape(all_scores, (1,4))
        temp_df = pandas.DataFrame(data=all_scores_inverted,
                      index=[key],
                      columns=['precision_in','precision_out', 'recall_in', 'recall_out'])
        scores_df = scores_df.append(temp_df)

    return scores_df

def make_graph(scores_df, modeler):
    #Setup
    sns.set(style="white", context="talk")
    f, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(8, 10.5), sharex=True)
    ax1.set_ylim([0,1])
    ax2.set_ylim([0,1])
    ax3.set_ylim([0,1])
    ax4.set_ylim([0,1])

    #set colors
    pal1 = "Reds_r"
    pal2 = "Oranges_r"
    pal3 = "Greens_r"
    pal4 = "Blues_r"

    #Sort data and assign consistent x
    scores_df = scores_df.sort_values(by="precision_out", ascending=False)
    x = scores_df.index.values

    #Make the subplots
    sns.barplot(x, scores_df['precision_in'], palette=pal1, ax=ax1)
    ax1.set_ylabel("In: Precision")

    sns.barplot(x, scores_df['recall_in'], palette=pal2, ax=ax2)
    ax2.set_ylabel("In: Recall")

    sns.barplot(x, scores_df['precision_out'], palette=pal3, ax=ax3)
    ax3.set_ylabel("Out: Precision")

    sns.barplot(x, scores_df['recall_out'], palette=pal4, ax=ax4)
    ax4.set_ylabel("Out: Recall")

    #Add annotations
    for ax in [ax1, ax2, ax3, ax4]:
        for p in ax.patches:
            ax.annotate(str(round(p.get_height(),2)), (p.get_x()+p.get_width()/2., p.get_height() * 1.1), ha='center')

    # Finalize the plot
    sns.despine(bottom=True)
    plt.setp(f.axes, yticks=[])
    plt.xticks(rotation=90)
    plt.tight_layout(h_pad=3)

    plt.savefig(modeler.version + "_confusion_comparisons.png")


if __name__ == '__main__':
    if len(sys.argv) > 1:
        pickle_name = sys.argv[1]
    else:
        pickle_name = 'modeler.pickle'

    modeler = run_models.load_modeler_pickle(pickle_name)
    scores_df = reformat_scores(modeler)
    make_graph(scores_df, modeler)

    print(modeler.answers.describe())
