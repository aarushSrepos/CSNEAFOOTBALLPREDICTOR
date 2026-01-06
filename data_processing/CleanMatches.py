from data_collection/DataCollection import HeadtoHeadMatches,SeasonRecord, GetTeamID, GetFutureMatches


def HeadtoHeadMatchStatistics(DateFrom, DateTo, Team1, Team2):
    #This code will find all the head to head matches in a given season and will make a tally of how many points each team acheived in total and to normalise it to a 0 to 1 scale,
    #each score tallied by each team is divided by the total number of points won across both teams
    Matches = HeadtoHeadMatches(DateFrom, DateTo, Team1, Team2)
    Team1Points = CalculateForm(Team1,DateFrom, DateTo, Matches)
    Team2Points = CalculateForm(Team2,DateFrom, DateTo, Matches)

    Team1PointShare = Team1Points/(Team1Points+Team2Points)
    Team2PointShare = Team2Points/(Team1Points+Team2Points)

    Record = [Team1PointShare, Team2PointShare]

    return Record




def CalculateForm(TeamID, DateFrom, DateTo, CustomMatchSet):
    #A custom match set is used when finding the form of teams in head to head matches as this is a filtered dataset
    if CustomMatchSet is not None:
        PastMatches = CustomMatchSet
    else:
        #using last 5 matches to calculate form
        PastMatches = SeasonRecord(DateFrom, DateTo, TeamID)
        PastMatches = PastMatches[:5]
    Form = 0
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
    Form = Form/15
    return Form



def SeasonGoalScoringRate(DateFrom, DateTo, TeamID ):
    matches = SeasonRecord(DateFrom, DateTo, TeamID, True)
    TotalGoalScored = 0
    for match in matches:
        if match['homeTeam']['id'] == TeamID:
            TotalGoalScored = TotalGoalScored + int(match['score']['fullTime']['home'])
        else:
            TotalGoalScored = TotalGoalScored + int(match['score']['fullTime']['away'])
    GoalRate = TotalGoalScored/len(matches)

    return GoalRate
def SeasonConcedingRate(DateFrom, DateTo, TeamID):
    matches = SeasonRecord(DateFrom, DateTo, TeamID, True)
    TotalConceded = 0
    for match in matches:
        if match['homeTeam']['id'] == TeamID:
            TotalConceded = TotalConceded + int(match['score']['fullTime']['away'])
        else:
            TotalConceded = TotalConceded + int(match['score']['fullTime']['home'])
    ConcedingRate = TotalConceded/len(matches)

    return ConcedingRate

def HomeAwayAdvantage(Location, Match):
    if Location == 'home':
        return 1
    elif Location == 'away':
        return 0
    else:
        return 0
 



def TeamFeatures(DateFrom, DateTo, Team1, Team2, FuturematchDate):
    CustomMatchSet = SeasonRecord(DateFrom, DateTo, TeamID, Past)
    H2H = HeadtoHeadMatchStatistics(DateFrom, DateTo, Team1, Team2)

    HAA1 = ''
    HAA2 = ''

    Futurematch = GetFutureMatches(Team1)
    UpcomingMatch = []
    for Fmatch in Futurematch:
        if Fmatch["utcDate"][:10] == FuturematchDate:
            if Fmatch['homeTeam']['id'] == Team1 or Fmatch['awayTeam']['id'] == Team1:
                if Fmatch['homeTeam']['id'] == Team2 or Fmatch['awayTeam']['id'] == Team2:
                    UpcomingMatch = Fmatch

    if UpcomingMatch['homeTeam']['id'] == Team1:
        HAA1 = 'home'
        HAA2 = 'away'
    else:
        HAA1 = 'away'
        HAA2 = 'home'

    
    #feature vector for team 1
    Form1 = CalculateForm(Team1, DateFrom, DateTo, CustomMatchSet)
    GSR1 = SeasonGoalScoringRate(DateFrom, DateTo, Team1)
    GCR1 = SeasonConcedingRate(DateFrom, DateTo, Team1)
    HAA1 = HAA1
    
    Team1Feature = [Form1,GSR1,GCR1,HAA1, H2H[0]]
    #Feature vector for team 2
    Form2 = CalculateForm(Team2, DateFrom, DateTo, CustomMatchSet)
    GSR1 = SeasonGoalScoringRate(DateFrom, DateTo, Team1)
    GCR1 = SeasonConcedingRate(DateFrom, DateTo, Team1)
    HAA2 = HAA2
    Team2Feature = [Form2,GSR2,GCR2,HAA2, H2H[1]]

    Features = [Team1Feature, Team2Feature]

    return Features


