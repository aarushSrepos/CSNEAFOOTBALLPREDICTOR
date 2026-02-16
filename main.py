from fastapi import FastAPI
from pydantic import BaseModel
from dataMaintenance.authentication import login, signup 
from database.DbManager import connect, Create, Read,Update, Delete 
from dataMaintenance.PredictionHandling import GetExistingPrediction, update_prediction, CreatePrediction, getPredictionForUI
from dataMaintenance.UserFavourites import add_favourite_team, remove_favourite_team, get_user_favourites, TeamIDtoTeamname
from data_collection.DataCollection import GetFutureMatches, GetMatches
import xgboost as xgb
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],#Allows requests from any device
    allow_credentials=True,#allows authorisation headers
    allow_methods=["*"],# allows all CRUD methods
    allow_headers=["*"],#allows HTTP headers
)

# All endpoints follow the same pattern:
# 1. Establish database connection
# 2. Call a dedicated backend function
# 3. Return a structured success/error response for the frontend


   
#to prevent requests being slowed down unnecessarily, I have loaded the model at the start of the program so that each endpoint which needs to use it can call it from here, as it is a gloabl variable here, this prevents uneccesary requests  
model = xgb.Booster()#initialises an empty xgboost model
model.load_model('MLprediction/models/Model.json')#loads the paramters made by training function


#The only time the frontend will send JSON data is during signup/login processes 
#so a pydantic model is required to serialise it into an instance of an object that can be used in python
class AuthRequest(BaseModel):
    email: str
    password: str



@app.post("/signup")
def signup_route(user: AuthRequest):#This assigns the JSON data to an insatnce of AuthRequest which inherits the BaseModel from pydantic which serialises the JSON data
    connection = connect()# a connection with the database is required for every transaction so this is seen in every endpoint here
    result = signup(connection, user.email, user.password)
    if result == -1:#adding a status allows the frontend to deal with the logic of either receiving data or not better
        return {"status": "error"}
    # Only return serializable fields
    return jsonable_encoder({
        "status": "success",
        "user": result
    })


@app.post("/login")
def login_route(user: AuthRequest):#same logic as signup
    connection = connect()
    result = login(connection, user.email, user.password)

    if result == -1:
        return {"status": "error"}

    return jsonable_encoder({
        "status": "success",
        "user": result
    })



@app.get('/getprediction/{matchid}')
def GetExistingPredictionRoute(matchid: int):# A pydantic model isnt used here as data is passed as a parameter
    connection = connect()
    Prediction = GetExistingPrediction(connection, matchid)
    if Prediction == -1:
        return {"status": "error"}
    else:
        return jsonable_encoder({"status": "success", "existingPrediction": Prediction})

@app.put('/updateprediction/{matchid}')
def updatePredictionRoute(matchid: int):
    connection = connect()
    UpdatedPrediction = update_prediction(connection, matchid, model)
    if UpdatedPrediction == -1:
        return {"status": "error"}
    else:
        return jsonable_encoder({"status": "success", "UpdatedPrediction": UpdatedPrediction})

@app.post('/createprediction/{matchid}')
def CreatePredictionRoute(matchid: int):
    connection = connect()
    NewPrediction = CreatePrediction(connection, matchid, model)
    if NewPrediction == -1:
        return {"status": "error"}
    else:
        return jsonable_encoder({"status": "success", "NewPrediction": NewPrediction})

@app.get('/getUIprediction/{matchid}')
def UIpredictionRoute(matchid: int):
    connection = connect()
    PredictionUI = getPredictionForUI(connection, matchid, model)
    if PredictionUI == -1:
        return {"status": "error"}
    else:
        return jsonable_encoder({"status": "success", "UIprediction": PredictionUI})


@app.post('/addfavouriteteam/{userid}/{teamid}')
def AddFavouriteTeamRoute(userid: int , teamid: int):
    connection = connect()
    AddedTeam = add_favourite_team(connection, userid, teamid)
    if AddedTeam == -1:
        return {"status": "error"}
    else:
        return jsonable_encoder({"status": "success", "NewTeamFavourite": AddedTeam})
   
@app.delete('/deletefavouriteteam/{userid}/{teamid}')
def RemoveFavouriteTeamRoute(userid: int, teamid: int):
    connection = connect()
    TeamRemoved = remove_favourite_team(connection, userid, teamid)
    if TeamRemoved == -1:
        return {"status": "error"}
    else:
        return jsonable_encoder({"status": "success", "TeamRemoved": TeamRemoved})

@app.get('/usersfavouriteteams/{userid}')
def GetUserFavouriteTeams(userid: int):
    connection = connect()
    UserFavourites = get_user_favourites(connection, userid)
    if UserFavourites == -1:
        return {"status": "error"}
    else:
        return jsonable_encoder({"status": "success", "UserFavourites": UserFavourites})   

@app.get('/teamidNameConversion/{teamid}')
def TeamIDtoTeamnameRoute(teamid: int):
    connection = connect()
    TeamName =TeamIDtoTeamname(connection, teamid)   
    if TeamName == -1:
        return {"status": "error"}
    else:
        return jsonable_encoder({"status": "success", "TeamName": TeamName})  

@app.get('/getmatches/{season}')
def getMatchesRoute(season: int):
    connection = connect()
    SeasonMatches = GetMatches(season)
    if SeasonMatches == -1:
        return {"status": "error"}
    else:
        return jsonable_encoder({"status": "success", "SeasonMatches": SeasonMatches})   
        
@app.get('/getfuturematches/{TeamID}/{Date}/{singularMatch}')
def FutureMatchRoute(TeamID: int, date: str, singularMatch: bool):
    connection = connect()
    FutureMatch = GetFutureMatches(TeamID, date, singularMatch)
    if FutureMatch == -1:
        return {"status": "error"}
    else:
        return jsonable_encoder({"status": "success", "FutureMatch": FutureMatch})   
