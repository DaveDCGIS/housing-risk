
class ManyModels:
    def __init__(self):

        self.models = {}  #expected: 'modelname':sklearn.model_instance
        self.X = numpy.array([[],[]]) #blank 2-d array, contains training data
        self.y = numpy.array([]) #blank 1-d array, contains training answers
        self.pipe = None #a pipeline for transforming this data. Should not contain a final model to predict.

        self.X_test = None
        self.y_test = None
        self.y_names = []
        self.answers = pandas.DataFrame() #Pandas dataframe where each row is a row of the test dataset, each column is a different model_list
        self.scores = {} #Nested dictionary of shape {'modelname': {'precision': #, 'recall': #, 'accuracy': #, 'f1': # }}

        self.version = ""
        self.notes = ""

    def fit(self, model_list=None):
        for key in model_list:
            self.models[key].fit(self.X, self.y)
        return self

    def predict(self, model_list=None):
        for key in model_list:
            self.answers[key] = self.models[key].predict(self.X_test)
            self.scores[key] = { }
            if self.y_test is not None:
                self.scores[key]['precision'] = metrics.precision_score(y_true = self.y_test, y_pred = self.answers[key].as_matrix(), average=None)
                self.scores[key]['recall'] = metrics.recall_score(y_true = self.y_test, y_pred=self.answers[key], average=None)
                self.scores[key]['accuracy'] = metrics.accuracy_score(y_true = self.y_test, y_pred=self.answers[key])
                self.scores[key]['f1'] = metrics.f1_score(y_true = self.y_test, y_pred=self.answers[key], average=None)
                self.scores[key]['classification_report'] = classification_report(y_true = self.y_test, y_pred = self.answers[key].as_matrix(), target_names=self.y_names)
        
        return self.answers




def run_models(dataframe, models_to_run = {}, undersample=False):

    modeler = data_utilities.ManyModels()
    dataframe = data_utilities.clean_dataframe(dataframe, debug = debug)
    #....
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=10, stratify = y)
    #...
    X_train = modeler.pipe.fit_transform(X_train)
    X_test = modeler.pipe.transform(X_test)

    if undersample == True:
        from imblearn.under_sampling import RandomUnderSampler
        rus = RandomUnderSampler()
        X_train, y_train = rus.fit_sample(X_train, y_train)
    #...
    modeler.fit(model_list=model_list)
    #...
    predicted_df = modeler.predict(model_list)

    return modeler


def get_custom_pipeline(col_names=None):
    #...

    pipeline = Pipeline([   ('imputer', Imputer())
                            ,('onehot', OneHotEncoder(categorical_features=mask, sparse=False))
                            ,('minmax', MinMaxScaler())
                            ])
    return pipeline



#Making our graphs
import seaborn as sns

if __name__ == '__main__':
    #...
    modeler = run_models.load_modeler_pickle(pickle_name)
    scores_df = reformat_scores(modeler)
    make_graph(scores_df, modeler)

#-------earlier in file--------

def reformat_scores(modeler):
    #Extract the scores needed and reformat them into the groupings needed by the graph
    #...
    return scores_df


def make_graph(scores_df, modeler, color = "Blues"):
    #Setup - Seaborn grouped bar chart!
    sns.set(style="white", context="talk")
    f, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(5, 1, figsize=(8, 10.5), sharex=True)

    #...

    #Sort data and assign consistent x
    scores_df = scores_df.sort_values(by="precision_out", ascending=False)
    x = scores_df.index.values

    #Make the subplots
    sns.barplot(x, scores_df['precision_in'], palette=pal1, ax=ax1)
    ax1.set_ylabel("In: Precision")

    #...

    plt.savefig(modeler.version + "_confusion_comparisons.png")






    modeler.models = {    "KNeighbors_default": sklearn.neighbors.KNeighborsClassifier()
                      , "RandomForest": sklearn.ensemble.RandomForestClassifier()
                      , "LogisticRegression": sklearn.linear_model.LogisticRegression(penalty='l1', C=0.1)
                      , "GaussianNB": GaussianNB()
                      , "SVC_rbf": SVC(kernel = 'rbf', probability = True, random_state = 0)
                      , "SVC_linear": SVC(kernel = 'linear', probability = True,  random_state = 0)
                      , "SVC_poly": SVC(kernel = 'poly', degree = 3, probability = True,  random_state = 0)
                      }

    #Different method for KNeighbors allows us to compare multiple k's
    for i in range(3,13):
        modeler.models["KNeighbors_{}".format(i)] = sklearn.neighbors.KNeighborsClassifier(n_neighbors=i)






Training data (30% training split)
Regular Samping: "In": 20552, "Out": 2682
Under Sampling:  "In": 2682, "Out": 2682