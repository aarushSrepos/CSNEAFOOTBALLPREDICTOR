from data_processing.CleanMatches import (CalculateForm, HeadtoHeadMatchStatistics, SeasonGoalScoringRate, SeasonConcedingRate, HomeAwayAdvantage, TeamFeatures)
from data_collection.DataCollection import GetTeamID, GetMatches
import time


"""
TEAM_ARSENAL = GetTeamID("Arsenal FC")
TEAM_CHELSEA = GetTeamID("Chelsea FC")

DateFrom = "2024-08-01"
DateTo = "2025-06-01"
FuturematchDate = '2026-03-01'
Seasons = [2023, 2024]

from MLprediction.prediction import train, evaluate_model, PredictFutureMatches
from MLprediction.Datasets import FuturematchDataset
print("Hello")
model, Ptrain, Ptest = train([2023])
print("1")
loss, acc = evaluate_model(
    model,
    Ptest,
    Ptest.get_label()
)

print("Test log loss:", loss)
print("Test accuracy:", acc)

X_future = FuturematchDataset('2025-11-1',TEAM_ARSENAL)
probs, preds, Futurematch = PredictFutureMatches(model, X_future)
sum = probs[0][0] + probs[0][1] + probs[0][2]
print(f"probabilities of match is {probs} and prediction is {preds}")

print(f"sum of probabilites for success critiria is {sum}")

print(f'model metadata:{model}')


"""
"""
from database.DbManager import connect,Create, Read, Update, Delete
from dataMaintenance.authentication import Passwordhash
conn = connect()

Password = Passwordhash('ABC123')

#createdUserData = Create(conn, "users", {'userid':1, 'email': 'test@email.com', 'passwordhash': f"{Password}"})


createdUserData = Create(conn, "users", {'userid':'1', 'email': 'test@email.com', 'passwordhash': f"{Password}"})
print(createdUserData)


ReadUserData = Read(conn, 'users', {'userid' :'1'})
print(ReadUserData)


UpdateUserData = Update(conn, 'users',{'email': 5}, {'email': 'test@email.com'})
print(UpdateUserData)


"""
"""
DeleteUserData = Delete(conn,'users', {'userid': '1'})
print(DeleteUserData)

"""





from dataMaintenance.PredictionHandling import GetExistingPrediction, update_prediction, CreatePrediction, getPredictionForUI
from database.DbManager import connect
import xgboost as xgb
from dataMaintenance.authentication import login, signup
from dataMaintenance.UserFavourites import add_favourite_team, remove_favourite_team, get_user_favourites, TeamIDtoTeamname

"""
connection = connect()
model = xgb.Booster()
model.load_model('MLprediction/models/Model.json')
print(CreatePrediction(connection, 537975, model))
print('')
print(GetExistingPrediction(connection, 537975))
print('')
print(update_prediction(connection, 537975, model))

"""

connection = connect()
print(connection)
# Signup
#user = signup(connection, 5, "Password123")
#print(user)
# Login
user = login(connection, "test@email.com", "Password123")
#print(user)
 
# Add favourite
#print(add_favourite_team(connection, user[0]['userid'], 57))
# Get favourites
#print(get_user_favourites(connection, '0'))

# Remove favourite
remove_favourite_team(connection, user[0]['userid'], 57)