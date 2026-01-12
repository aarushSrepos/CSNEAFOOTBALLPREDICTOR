from data_processing.CleanMatches import (CalculateForm, HeadtoHeadMatchStatistics, SeasonGoalScoringRate, SeasonConcedingRate, HomeAwayAdvantage, TeamFeatures)
from data_collection.DataCollection import GetTeamID
import time
TEAM_ARSENAL = GetTeamID("Arsenal FC")
TEAM_CHELSEA = GetTeamID("Chelsea FC")

DateFrom = "2024-08-01"
DateTo = "2025-06-01"
FuturematchDate = '2026-03-01'



ChelseaFeatures = TeamFeatures(DateFrom, DateTo, TEAM_ARSENAL, TEAM_CHELSEA, FuturematchDate, False)
print('Chelsea features', ChelseaFeatures)
ArsenalFeatures = TeamFeatures(DateFrom, DateTo, TEAM_ARSENAL, TEAM_CHELSEA, FuturematchDate, True)
print('Arsenal features', ArsenalFeatures)
