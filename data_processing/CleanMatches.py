from data_collection.DataCollection import (HeadtoHeadMatches,SeasonRecord, GetTeamID, GetFutureMatches, GetMatches)
import time


def HeadtoHeadMatchStatistics(DateFrom, DateTo, Team1, Team2):
    #This code will find all the head to head matches in a given season and will make a tally of how many points each team acheived in total and to normalise it to a 0 to 1 scale,
    #each score tallied by each team is divided by the total number of points won across both teams
    
    Matches = HeadtoHeadMatches(DateFrom, DateTo, Team1, Team2)
    Team1Points = CalculateForm(Team1,DateFrom, DateTo, Matches)
    Team2Points = CalculateForm(Team2,DateFrom, DateTo, Matches)
    if type(Matches) == bool or type(Team1Points) == bool or type(Team2Points) == bool:
        return True
    else:
        if Team1Points != 0 and Team2Points:
            Team1PointShare = Team1Points/(Team1Points+Team2Points)
            Team2PointShare = Team2Points/(Team1Points+Team2Points)
        else:
            Team1PointShare = 0.5
            Team2PointShare = 0.5
        Record = [Team1PointShare, Team2PointShare]

        return Record




def CalculateForm(TeamID, DateFrom, DateTo, CustomMatchSet):
    #A custom match set is used when finding the form of teams in head to head matches as this is a filtered dataset
    if type(CustomMatchSet) == bool:
        return True
    else:
        if type(CustomMatchSet) is not None :
            PastMatches = CustomMatchSet[-5:]
        else:
            #using last 5 matches to calculate form
            PastMatches = SeasonRecord(DateFrom, DateTo, TeamID, True)
            PastMatches = PastMatches[-5:]
    

    if type(PastMatches) == bool:
        return True
    else: 
        Form = 0.0
        for match in PastMatches:
            HomeID = match["homeTeam"]["id"]
            AwayID = match["awayTeam"]["id"]
            winner = match["score"]["winner"]

            if winner == "DRAW":
                Form = Form + 1

            if winner == "HOME_TEAM":
                if HomeID == TeamID:
                    Form = Form + 3

            if winner == "AWAY_TEAM":
                if AwayID == TeamID:
                    Form = Form + 3
        #Form is divided by 15 as 15 is the maximum number of points you can win in 5 games. This normalises Form to a 0 to 1 scale
        Form = Form / 15
        return Form



def SeasonGoalScoringRate(DateFrom, DateTo, TeamID ):
    #Approximation for xG
    matches = SeasonRecord(DateFrom, DateTo, TeamID, True)
    TotalGoalScored = 0
    if type(matches) == bool:
        return True
    else:
        for match in matches:
            if match['homeTeam']['id'] == TeamID:
                TotalGoalScored = TotalGoalScored + int(match['score']['fullTime']['home'])
            else:
                TotalGoalScored = TotalGoalScored + int(match['score']['fullTime']['away'])
        #multiplied by 10 as this normalises the GSR to values between 0 and 1 as, historically, it is highly unlikely to have a goal scoring rate of >10 in the premier league,
        GoalRate = TotalGoalScored/(10*len(matches))
        return GoalRate


def SeasonConcedingRate(DateFrom, DateTo, TeamID):
    #Approximation for xGA
    matches = SeasonRecord(DateFrom, DateTo, TeamID, True)
    TotalConceded = 0
    if type(matches) == bool:
        return True
    else:
        for match in matches:
            if match['homeTeam']['id'] == TeamID:
                TotalConceded = TotalConceded + int(match['score']['fullTime']['away'])
            else:
                TotalConceded = TotalConceded + int(match['score']['fullTime']['home'])
        ConcedingRate = TotalConceded/(10*len(matches))

        return ConcedingRate

def HomeAwayAdvantage(Home):
    if Home:
        return 1
    else:
        return 0
 



def TeamFeatures(DateFrom, DateTo, Team1, Team2, FuturematchDate, ReturnTeam1):

    #Get past match data to calculate form
    CustomMatchSet1 = SeasonRecord(DateFrom, DateTo, Team1, True)
    CustomMatchSet2 = SeasonRecord(DateFrom, DateTo, Team2, True)

    #Calculating what share of overall points each team has as a fraction of combined points
    H2H = HeadtoHeadMatchStatistics(DateFrom, DateTo, Team1, Team2)
    #'HAA'-Home away advantage
    HAA1 = False
    HAA2 = False

    Futurematch = GetFutureMatches(Team1)
    UpcomingMatch = []
    if type(Futurematch) == bool:
        return "Rate limit error"
    else:
        for Fmatch in Futurematch:
            if Fmatch["utcDate"][:10] == FuturematchDate:
                if Fmatch['homeTeam']['id'] == Team1 or Fmatch['awayTeam']['id'] == Team1:
                    if Fmatch['homeTeam']['id'] == Team2 or Fmatch['awayTeam']['id'] == Team2:
                        UpcomingMatch = Fmatch

    if UpcomingMatch['homeTeam']['id'] == Team1:
        HAA1 = True
        HAA2 = False
    else:
        HAA1 = False
        HAA2 = True

    if ReturnTeam1:
        #Feature vector for team 1
        Form1 = CalculateForm(Team1, DateFrom, DateTo, CustomMatchSet1)
        GSR1 = SeasonGoalScoringRate(DateFrom, DateTo, Team1)
        GCR1 = SeasonConcedingRate(DateFrom, DateTo, Team1)
        HAA1 = HomeAwayAdvantage(HAA1)
        if type(Form1) == bool or type(GSR1) == bool or type(GCR1) == bool or type(HAA1) == bool:
            return "Rate limit error"
        else:

            Team1Feature = [Form1, GSR1, GCR1, HAA1, H2H[0]]
            return Team1Feature
    else:
        #Feature vector for team 2
        Form2 = CalculateForm(Team2, DateFrom, DateTo, CustomMatchSet2)
        GSR2 = SeasonGoalScoringRate(DateFrom, DateTo, Team2)
        GCR2 = SeasonConcedingRate(DateFrom, DateTo, Team2)
        HAA2 = HomeAwayAdvantage(HAA2)
        if type(Form2) == bool or type(GSR2) == bool or type(GCR2) == bool or type(HAA2) == bool:
            return "Rate limit error" 
        else:  
            Team2Feature = [Form2,GSR2,GCR2,HAA2, H2H[1]]
            return Team2Feature     

def OverallTeamFeature(DateFrom, DateTo, Team1, Team2, FuturematchDate):
    Team1Feature = TeamFeatures(DateFrom, DateTo, Team1, Team2, FuturematchDate, True)
    time.sleep(60)
    Team2Feature = TeamFeatures(DateFrom, DateTo, Team1, Team2, FuturematchDate, False)

    OverallTeamFeature = []
    OverallTeamFeature.append(Team1Feature, Team2Feature)
    return OverallTeamFeature


def MatchFeatureset(DateFrom, DateTo):

