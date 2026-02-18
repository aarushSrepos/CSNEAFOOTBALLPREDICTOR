from database.DbManager import connect, Create, Read, Update, Delete
from datetime import datetime, timezone
from MLprediction.Datasets import FuturematchDataset
from MLprediction.prediction import PredictFutureMatches
def GetExistingPrediction(connection, match_id):
    prediction = Read(connection, 'predictions', {'matchid': match_id})
    return prediction

def update_prediction(connection, match_id, model):
    Match = Read(connection, 'matches', {'matchid': match_id})
    MatchDate = Match[0]['match_date']
    Futurematch = FuturematchDataset(f'{MatchDate}',int(Match[0]['hometeamid']))
    prob = PredictFutureMatches(model, Futurematch)
    UpdatedPrediction = Update(connection, 'predictions', {'matchid': match_id}, { 'winprob':prob[0][0], 'drawprob':prob[0][1], 'lossprob': prob[0][2]})
    return UpdatedPrediction

def CreatePrediction(connection, match_id, model):
    Match = Read(connection, 'matches', {'matchid': match_id})
    print(Match)
    print(Match[0]['hometeamid'])
    print(Match[0]['match_date'])
    MatchDate = Match[0]['match_date']
    Futurematch = FuturematchDataset(f'{MatchDate}',int(Match[0]['hometeamid']))
    print(f"This is the future match dataset{Futurematch}")
    prob = PredictFutureMatches(model, Futurematch)
    print(f"this is the probability set {prob}")
    timecreated = datetime.now(timezone.utc).date()
    print(f" This is the time created {timecreated}")
    NewPrediction = Create(connection, 'predictions', 
    {'matchid': match_id, 'winprob':prob[0][0], 'drawprob':prob[0][1], 
    'lossprob': prob[0][2], 'predictedhomegoals': None, 'predictedawaygoals': None,
     'timecreated': timecreated})
    print(f"This is the new prediction {NewPrediction}")
    return NewPrediction


def getPredictionForUI(connection, match_id, model):
    
    Prediction = GetExistingPrediction(connection, match_id)
    if Prediction == -1:
        NewPrediction = CreatePrediction(connection, match_id, model)
        return NewPrediction
    else:
        return Prediction



def SavePrediction(connection, prob, match_id):
    timecreated = datetime.now(timezone.utc).date()
    SavePrediction = Create(connection, 'predictions', 
    {'matchid': match_id, 'winprob':prob[0], 'drawprob':prob[1], 
    'lossprob': prob[2], 'predictedhomegoals': None, 'predictedawaygoals': None,
     'timecreated': timecreated})



def SaveMatch(connection, match_id, home_id, away_id, match_date):
    SavedMatch = Create(connection, 'matches', {
        'matchid': match_id,
        'hometeamid': home_id,
        'awayteamid': away_id,
        'match_date': match_date,
        'season': 2025
    })

