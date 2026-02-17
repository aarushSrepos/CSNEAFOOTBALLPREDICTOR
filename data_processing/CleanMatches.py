from data_collection.DataCollection import (HeadtoHeadMatches,SeasonRecord, GetTeamID, GetFutureMatches, GetMatches)
import time


def HeadtoHeadMatchStatistics(DateFrom, DateTo, Team1, Team2, matches):
    #This code will find all the head to head matches in a given season and will make a tally of how many points each team acheived in total and to normalise it to a 0 to 1 scale,
    #each score tallied by each team is divided by the total number of points won across both teams
    
    Matches = HeadtoHeadMatches(DateFrom, DateTo, Team1, Team2, matches)
    Team1Points = CalculateForm(Team1,DateFrom, DateTo, Matches)
    Team2Points = CalculateForm(Team2,DateFrom, DateTo, Matches)
    if Matches == -1 or Team1Points == -1 or Team2Points == -1:
        return 0 # this can be 0 as early in the season it is possible that teams may not have played a match
    else:
        if Team1Points != 0 and Team2Points != 0:
            Team1PointShare = Team1Points/(Team1Points+Team2Points)
            Team2PointShare = Team2Points/(Team1Points+Team2Points)
        else:
            Team1PointShare = 0.5
            Team2PointShare = 0.5
        Record = [Team1PointShare, Team2PointShare]

        return Record




def CalculateForm(TeamID, DateFrom, DateTo, CustomMatchSet):
    #A custom match set is used when finding the form of teams in head to head matches as this is a filtered dataset
    if CustomMatchSet == -1:
        return -1
    else:
        if CustomMatchSet is not None:
            PastMatches = CustomMatchSet[-5:]
        else:
            #using last 5 matches to calculate form
            PastMatches = SeasonRecord(DateFrom, DateTo, TeamID, True, CustomMatchSet)
            PastMatches = PastMatches[-5:]
    

    if PastMatches == -1:
        return -1
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



def SeasonGoalScoringRate(DateFrom, DateTo, TeamID, matches):
    #Approximation for xG
    matches = SeasonRecord(DateFrom, DateTo, TeamID, True, matches)
    TotalGoalScored = 0
    if matches == -1:
        return -1
    else:
        for match in matches:
            if match['homeTeam']['id'] == TeamID:
                TotalGoalScored = TotalGoalScored + int(match['score']['fullTime']['home'])
            else:
                TotalGoalScored = TotalGoalScored + int(match['score']['fullTime']['away'])
        #multiplied by 10 as this normalises the GSR to values between 0 and 1 as, historically, it is highly unlikely to have a goal scoring rate of >10 in the premier league,
        GoalRate = TotalGoalScored/(10*len(matches))
        return GoalRate


def SeasonConcedingRate(DateFrom, DateTo, TeamID, matches):
    #Approximation for xGA
    matches = SeasonRecord(DateFrom, DateTo, TeamID, True, matches)
    TotalConceded = 0
    if matches == -1:
        return -1
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
 



def TeamFeatures(DateFrom, DateTo, Team1, Team2, FuturematchDate, ReturnTeam1, context, matches):
    #it is possible here to replace DateTO with FuturematchDate as the only purpose of DateTo is for finding the form,however,
    #keeping separate variables here allows for predictions further into the future to be made 
    #Get past match data to calculate form

    CustomMatchSet1 = SeasonRecord(DateFrom, DateTo, Team1, True, matches)
    CustomMatchSet2 = SeasonRecord(DateFrom, DateTo, Team2, True, matches)
    if CustomMatchSet1 == -1 or CustomMatchSet2 == -1:
        return -1
    if len(CustomMatchSet1) < 1 or len(CustomMatchSet2) < 1:
        return -1
    #Calculating what share of overall points each team has as a fraction of combined points
    H2H = HeadtoHeadMatchStatistics(DateFrom, DateTo, Team1, Team2, matches)#
    #'HAA'-Home away advantage
    HAA1 = False
    HAA2 = False
    UpcomingMatch = []
    if context == 0 and Team2 == None:# if context is 0 then this is an actual future prediciton but otherwise it is training data and so all matches will have been scheduled to finished
        UpcomingMatch, Team2 = GetFutureMatches(Team1, DateTo, True)

    else:
        Futurematch = SeasonRecord(DateFrom, DateTo, Team1, True, matches)
        if Futurematch == -1:
            return -1
        else:
            for Fmatch in Futurematch:
                if Fmatch["utcDate"][:10] == FuturematchDate:
                    if Fmatch['homeTeam']['id'] == Team1 or Fmatch['awayTeam']['id'] == Team1:
                        if Fmatch['homeTeam']['id'] == Team2 or Fmatch['awayTeam']['id'] == Team2:
                            UpcomingMatch = Fmatch
    if UpcomingMatch == []:
        return -1
        
    else:
        if UpcomingMatch['homeTeam']['id'] == Team1:
            HAA1 = True
            HAA2 = False
        else:
            HAA1 = False
            HAA2 = True

    if ReturnTeam1:
        #Feature vector for team 1
        Form1 = CalculateForm(Team1, DateFrom, DateTo, CustomMatchSet1)
        GSR1 = SeasonGoalScoringRate(DateFrom, DateTo, Team1, matches)
        GCR1 = SeasonConcedingRate(DateFrom, DateTo, Team1, matches)
        HAA1 = HomeAwayAdvantage(HAA1)
        if Form1 == -1 or GSR1 == -1 or GCR1 == -1:
            return -1
        else:

            Team1Feature = [Form1, GSR1, GCR1, HAA1, H2H[0]]
            return Team1Feature
    else:
        #Feature vector for team 2
        Form2 = CalculateForm(Team2, DateFrom, DateTo, CustomMatchSet2)
        GSR2 = SeasonGoalScoringRate(DateFrom, DateTo, Team2, matches)
        GCR2 = SeasonConcedingRate(DateFrom, DateTo, Team2, matches)
        HAA2 = HomeAwayAdvantage(HAA2)
        if Form2 == -1 or GSR2 == -1 or GCR2 == -1:
            return -1 
        else:  
            Team2Feature = [Form2,GSR2,GCR2,HAA2, H2H[1]]
            return Team2Feature     



def OverallTeamFeature(DateFrom, DateTo, Team1, Team2, FuturematchDate,context, matches):
    if FuturematchDate is None:
        FuturematchDate = DateTo
    Team1Feature = TeamFeatures(DateFrom, DateTo, Team1, Team2, FuturematchDate, True, context, matches)
    Team2Feature = TeamFeatures(DateFrom, DateTo, Team1, Team2, FuturematchDate, False, context, matches)
    if Team1Feature == -1 or Team2Feature == -1:
        return []
    OverallTeamFeature = []
    OverallTeamFeature = Team1Feature + Team2Feature
    return OverallTeamFeature



