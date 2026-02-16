import requests
API_KEY = "e9eb18b48bab496db3160863769ac54d"
BASE_URL = "https://api.football-data.org/v4"
headers = {"X-Auth-Token": API_KEY}

def GetTeamID(TeamName):
    RateLimit = False
    url = f"{BASE_URL}/competitions/PL/teams"
    response = requests.get(url, headers=headers)
    print(response)
    if response.status_code == 200:
      teams = response.json()["teams"]
      TeamID = 0
      for team in teams:
          if TeamName in team["name"]:
              TeamID = team["id"]

      return TeamID
    else:
      return -1
      
       


def HeadtoHeadMatches(DateFrom, DateTo, Team1, Team2, matches):
    RateLimit = False
    url = f"{BASE_URL}/teams/{Team1}/matches"
    conditions = {
    "status": "FINISHED",
    "dateFrom": f'{DateFrom}',
    "dateTo": f'{DateTo}'
    }
    if matches is not None:
      HeadtoHeadMatchList = []
      for match in matches:
          home = match["homeTeam"]["id"]
          away = match["awayTeam"]["id"]
          if home == Team1 or away == Team2:
              HeadtoHeadMatchList.append(match)
          elif home == Team2 or away == Team1:
              HeadtoHeadMatchList.append(match)
          else:
              continue

      return HeadtoHeadMatchList
    
    response = requests.get(url, headers=headers, params=conditions)

    if response.status_code == 200:
      matches = response.json()["matches"]
      HeadtoHeadMatchList = []
      for match in matches:
          home = match["homeTeam"]["id"]
          away = match["awayTeam"]["id"]
          if home == Team1 and away == Team2:
              HeadtoHeadMatchList.append(match)
          elif home == Team2 and away == Team1:
              HeadtoHeadMatchList.append(match)
          else:
              continue

      return HeadtoHeadMatchList
    else:
      return -1



def SeasonRecord(DateFrom, DateTo, TeamID, Past, matches):
      
    RateLimit = False
    url = f"{BASE_URL}/teams/{TeamID}/matches"
    if Past == True:
      conditions = {
      "status": "FINISHED",
      "dateFrom": f'{DateFrom}',
      "dateTo": f'{DateTo}'
      }
    else:
      conditions = {
        "status": "SCHEDULED",
        }
    
    if matches is not None:
      TeamMatches = []
      for match in matches:
        if match["homeTeam"]["id"] == TeamID or match["awayTeam"]["id"] == TeamID:
          TeamMatches.append(match)
      return TeamMatches
    
    response = requests.get(url, headers=headers, params=conditions)
    if response.status_code == 200:
      matches = response.json()["matches"]
      return matches
    else:
      return -1


def GetFutureMatches(TeamID, Date, singularMatch):
  if TeamID is not None:
      Futurematches = SeasonRecord(None, None, TeamID, False, None)
      if singularMatch == True:
            
        WantedMatch = []

        for match in Futurematches:
          if match["utcDate"][:10] == Date and (match["homeTeam"]["id"] == TeamID or match["awayTeam"]["id"] == TeamID):
              WantedMatch = match
              if match["homeTeam"]["id"] == TeamID:
                return WantedMatch, match["awayTeam"]["id"]
              else:
                return WantedMatch, match["homeTeam"]["id"]
                
      else:
            return Futurematches
  else:
      Futurematches = SeasonRecord(None, None, None, False, None)
      return Futurematches


def GetMatches(season):
    url = f"{BASE_URL}/competitions/PL/matches"
    conditions = {
        "season": f"{season}"
    }
    response = requests.get(url, headers=headers, params=conditions)

    if response.status_code == 200:
        return response.json()["matches"]
    else:
        return -1
