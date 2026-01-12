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
      RateLimit = True
      return RateLimit
      
       


def HeadtoHeadMatches(DateFrom, DateTo, Team1, Team2):
    RateLimit = False
    url = f"{BASE_URL}/teams/{Team1}/matches"
    conditions = {
    "status": "FINISHED",
    "dateFrom": f'{DateFrom}',
    "dateTo": f'{DateTo}'
    }
    response = requests.get(url, headers=headers, params=conditions)

    if response.status_code == 200:
      matches = response.json()["matches"]
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
    else:
      RateLimit = True
      return RateLimit



def SeasonRecord(DateFrom, DateTo, TeamID, Past):
      
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
          
    response = requests.get(url, headers=headers, params=conditions)
    if response.status_code == 200:
      matches = response.json()["matches"]
      return matches
    else:
      RateLimit = True
      return RateLimit

    return matches


def GetFutureMatches(TeamID):
  if TeamID is not None:
      Futurematches = SeasonRecord(None, None, TeamID, False)
      return Futurematches
  else:
    url = f'{BASE_URL}/competitions/PL/matches'
    params = {
        "status": "SCHEDULED",
    }
    response = requests.get(url, headers=headers, params=params)
    Futurematches = response.json()["matches"]
    return Futurematches


def GetMatches(season):
    url = f"{BASE_URL}/competitions/PL/matches"
    conditions = {
        "season": season
    }
    response = requests.get(url, headers=headers, params=conditions)

    if response.status_code == 200:
        return response.json()["matches"]
    else:
        return True
