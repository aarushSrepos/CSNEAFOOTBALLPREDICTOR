import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import log_loss
from MLprediction.Datasets import MSeasonDataset, FuturematchDataset
from sklearn.metrics import accuracy_score
import numpy as np


def train(Seasons):
    
    Prediction, Outcome = MSeasonDataset(Seasons) #this is the training/test dataset 
    print(Prediction)
    print(Outcome)
    Prediction = np.array(Prediction, dtype=float)
    Outcome = np.array(Outcome, dtype=int)
    Predictiontrain, Predictiontest, Outcometrain, Outcometest = train_test_split(
    Prediction, Outcome, test_size=0.2, random_state=67)
    # random state takes either None or any integer, if an integer is input then the model will produce replicable results
    #test size means 80% of data will be used for training and 20% will be used for tests.
    print(type(Predictiontrain))
    print(len(Predictiontrain))
    print(type(Predictiontrain[0]))

    Ptrain = xgb.DMatrix(Predictiontrain, label=Outcometrain) # attaches feature vector for a specific match to the correct outcome
    Ptest = xgb.DMatrix(Predictiontest, label=Outcometest)# does the same function as Ptrain but for test data

    parameters = {
        'objective' : 'multi:softprob',
        # this tells xGboost what it is trying to predict, here it is predicting the probabilities of multiple outcomes(win,draw,lose)
        'num_class' : 3,
        #this is the number of outcomes xGboost predicts probabilties for
        "eval_metric": "mlogloss",
        # this metric allows the model to evaluate a tree's output to the log of the label, as the output of each tree is not actually a probability but a correction
        'learning_rate': 0.05, 
        #this dictates how aggresive the corrections from each tree will be, I have chosen a small learning rate due to large dataset and relatively large variance of outcomes
        'max_depth': 3,
         # essentially how many "if statements" a tree has, see Development section for more explanation on how I came up with this number
        'subsample': 0.8, 
        # to prevent overfitting each tree does not see the same samples, 
        #so each tree will see 70% of all the sample rows, this means that most trees will see mostly the same samples but there may be some variation in what they see
        #I have chosen 80% as the sample size is relatively small for what is considered to be a good size for a machine learning model
        'colsample_bytree': 1,
        #In most cases each tree will not see all metrics in order to prevent overfitting, but due to only having 10 features in our feature vector, it is imperative that all metrics are seen.
        "verbosity": 1# This is set to 1 to see how the model improves in testing by printing the logloss for every prediction, but when stakeholders use the app this will be turned to False
        }
    TreeNums = 1000 # this is maximum number of trees the model will use

    OutcomeMatchModel = xgb.train(
        params=parameters,
        dtrain=Ptrain,# training dataset
        num_boost_round=TreeNums,
        evals=[(Ptrain, 'train'), (Ptest, 'test')],
        early_stopping_rounds=20,#if the logloss has not improved after 20 rounds then no further trees are created.
      )

    OutcomeMatchModel.save_model("MLprediction/models/Model.json")


    return OutcomeMatchModel, Ptrain, Ptest


def evaluate_model(model, Ptest, Outcometest):
    Outcomes = model.predict(Ptest) 
    loss = log_loss(Outcometest, Outcomes)

    predictions = Outcomes.argmax(axis=1)
    accuracy = accuracy_score(Outcometest, predictions)

    return loss, accuracy


def PredictFutureMatches(model, Futurematch):
    FMatch = xgb.DMatrix(Futurematch)
    probs = model.predict(FMatch)
    preds = probs.argmax(axis=1)#outputs index of highest probability
    return probs
