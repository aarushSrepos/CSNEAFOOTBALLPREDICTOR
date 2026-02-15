from database.DbManager import connect, Create, Read, Update, Delete


def add_favourite_team(connection, userid, teamid):
    NewFav = Create(connection, 'userfavourites', {'userid': userid, 'teamid': teamid})
    return NewFav

def remove_favourite_team(connection, userid, teamid):
    DeleteFav = Delete(connection, 'userfavourites', {'userid': userid, 'teamid': teamid})
    return DeleteFav
    
def get_user_favourites(connection, userid):
    Favs = Read(connection, 'userfavourites', {'userid': userid})
    return Favs


def TeamIDtoTeamname(connection, teamid):
    TeamName = Read(connection, 'teams', {'teamid': teamid})
    return TeamName


