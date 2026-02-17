from datetime import datetime, timedelta
from data_collection.DataCollection import (GetMatches)
from data_processing.CleanMatches import (OverallTeamFeature)
import xgboost as xgb
from sklearn.model_selection import train_test_split
import numpy as np

def FiveWeeks(MatchDate):
    #Returns Date 5 weeks before match date by changing date into datetime object and then subtracting 35 days
    MatchDate = datetime.strptime(MatchDate, "%Y-%m-%d")
    DateFrom = MatchDate - timedelta(weeks=5)
    return DateFrom.strftime("%Y-%m-%d")


def Result(match):
    winner = match["score"]["winner"]
    if winner == "HOME_TEAM":
        return 0
    elif winner == "DRAW":
        return 1
    else:
        return 2



def BuildDataset(season):
    skipped = 0
    kept = 0
    #obtaining all matches in a season to build a feature vector and label for all
    matches = GetMatches(season)
    if matches == -1:
        return np.array([]), np.array([])
    X = []
    y = []

    for match in matches:
        if match["status"] != "FINISHED":
            continue
            #loops onto next match if the match hasn't been played

        MatchDate = match["utcDate"][:10]
        #the date of the match stored by football-data gives the time aswell but I only need the date so i am extracting just that
        DateFrom = FiveWeeks(MatchDate)
        # gives date 5 weeks before match which is used to calculate features in feature vector by essentially looking at only past 5 games

        HomeID = match["homeTeam"]["id"]
        AwayID = match["awayTeam"]["id"]

        featureVector = OverallTeamFeature(DateFrom, MatchDate, HomeID, AwayID, None, 1, matches)
        if featureVector == []:
            skipped += 1
            continue
        label = Result(match)
        kept += 1
        X.append(featureVector)
        y.append(label)
    print(f"number skipped is {skipped} and number kept is {kept}")
    print(type(X), type(X[0]), len(X[0]))

    return np.array(X), np.array(y)

def MSeasonDataset(seasons):
    #this function combines multiple seasons into a single dataset, 
    #the reason is that 2023 and 2024 season will both be used for training/testing 
    #and 2025 will be used for future predictions as the season is ongoing
    X,y = [], []

    for season in seasons:
        x, Y = BuildDataset(season)
        X.extend(x)
        y.extend(Y)

    return np.array(X), np.array(y)

def FuturematchDataset(Date, HomeID, AwayID):

    DateFrom = FiveWeeks(Date)
    print(DateFrom)
    featureVector = OverallTeamFeature(DateFrom, Date, HomeID, AwayID,None,0, None)
    
    return np.array([featureVector])
