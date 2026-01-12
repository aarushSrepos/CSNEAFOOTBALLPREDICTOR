import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import log_loss


def OutcomeProbabilities(TeamFeatures,):

Predictiontrain, Predictiontest, Outcometrain, Outcometest = train_test_split(
  Prediction, Outcome, test_size=0.2, random_state=67
)


Ptrain = xgb.DMatrix(Predictiontrain, label=Outcometrain)
Ptest = xgb.DMatrix(Predictiontest, label=Outcometest)

parameters = {
    'objective' : 'multi:softprob',
    "evaluation_metric": "logloss",
    'eta': 0.05,
    'max_depth': 4,
    'subsample': 0.7,
    'colsample_bytree': 1,
    'lambda': 1.0
}

TreeNums = 25


ClassificationMatchModel = xgb.train(
    params=params,
    dtrain=Ptrain,
    num_boost_round=TreeNums,
    evals=[(Ptrain, 'train'), (Ptest, 'test')],
    verbose_eval=5
)

MatchPredict = ClassificationMatchModel.predict(Ptest)
