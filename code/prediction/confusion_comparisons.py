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

        #Add guess/value counts
        value_count_series = modeler.answers[key].value_counts().transpose()
        value_count_ids = modeler.answers[key].value_counts().index.tolist()

        #TODO this could be refactored to use dictionary and for loops if we ever reuse this code for a mult-class problem
        most_guessed = value_count_ids[0]
        most_guessed_column_name = "guesses_for_{}".format(most_guessed)
        most_guessed_count = value_count_series[0]
        try:
            second_guessed = value_count_ids[1]
            second_guessed_column_name = "guesses_for_{}".format(second_guessed)
            second_guessed_count = value_count_series[1]
        except IndexError:
            second_guessed = 0
            second_guessed_column_name = "guesses_for_1"
            second_guessed_count = 0

        #temp_df = temp_df.assign(guesses_in = value_count_series[0])

        temp_df[most_guessed_column_name] = pandas.Series(most_guessed_count, index=temp_df.index)
        temp_df[second_guessed_column_name] = pandas.Series(second_guessed_count, index=temp_df.index)
        temp_df = temp_df.assign(percent_guesses_out = temp_df['guesses_for_1'] / (temp_df['guesses_for_1'] + temp_df['guesses_for_0'])) #1 = out per meta data. TODO pull class id's in from meta data here instead of hard-coded
        scores_df = scores_df.append(temp_df)

    print(scores_df)
    return scores_df

def make_graph(scores_df, modeler, color = "Blues"):
    #Setup
    sns.set(style="white", context="talk")
    f, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(5, 1, figsize=(8, 10.5), sharex=True)
    ax1.set_ylim([0,1])
    ax2.set_ylim([0,1])
    ax3.set_ylim([0,1])
    ax4.set_ylim([0,1])
    ax5.set_ylim([0,1])

    #set colors
    color = color + "_r"
    pal1 = color
    pal2 = color
    pal3 = color
    pal4 = color
    pal5 = "Oranges_r"

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

    sns.barplot(x, scores_df['percent_guesses_out'], palette=pal5, ax=ax5)
    ax5.set_ylabel("Out freq frac")

    #Add annotations
    for ax in [ax1, ax2, ax3, ax4, ax5]:
        for p in ax.patches:
            #See options in the documentation for Axes.annotate. Additional keywords are passed along to matplotlib.text.Text. http://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.annotate.html#matplotlib.axes.Axes.annotate
            ax.annotate(str(round(p.get_height(),2)), (p.get_x()+p.get_width()/2., p.get_height() * 1.1), ha='center', size='x-small')

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
    make_graph(scores_df, modeler, color="Greens")

    print("How many times was each category actually seen?")
    print("Actual count: ")
    print(pandas.Series(modeler.y_test).value_counts())
    actual_percent_out = pandas.Series(modeler.y_test).value_counts()[1] / (pandas.Series(modeler.y_test).value_counts()[0] + pandas.Series(modeler.y_test).value_counts()[1])  #TODO hacky not memory friendly code!!
    print("Actual percent outs: {}".format(actual_percent_out))
