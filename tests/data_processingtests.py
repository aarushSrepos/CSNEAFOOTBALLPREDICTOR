from data_processing.CleanMatches import CalculateForm, HeadtoHeadMatchStatistics
from data_collection.DataCollection import GetTeamID

TEAM_ARSENAL = GetTeamID("Arsenal FC")
TEAM_CHELSEA = GetTeamID("Chelsea FC")

DATE_FROM = "2024-08-01"
DATE_TO = "2024-12-31"

form = CalculateForm(TEAM_ARSENAL, DATE_FROM, DATE_TO, None)
print("Form:", form)

h2h = HeadtoHeadMatchStatistics(DATE_FROM, DATE_TO, TEAM_ARSENAL, TEAM_CHELSEA)
print("Head-to-head:", h2h)
