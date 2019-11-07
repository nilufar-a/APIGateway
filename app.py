from flask import Flask
from functools import wraps
from flask import abort
from flask import request
import requests
import jsonify
from flask import render_template

app = Flask(__name__)

authentication_url = ""
game_engine_url = ""
scores_leader_url = ""
match_making_url = ""
map_editor_url = ""

# ______________________________AUTHETICATION_____________________________________________
@app.route("/login", methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    response = requests.post(authentication_url + "login", data={'username': username, 'password': password})

    return str(response.status_code)


@app.route("/forgotPassword", methods=['POST'])
def forgot():
    username = request.form.get('username')
    response = requests.post(authentication_url + "forgotPassword", data={'username': username})
    return str(response.status_code)


@app.route("/changePassword", methods=['POST'])
def change():
    token = request.form.get('token')
    oldpassword = request.form.get('oldpassword')
    newpassword = request.form.get('newpassword')
    response = requests.post(authentication_url + "changePassword", data={'token': token, 'oldpassword': oldpassword, 'newpassword': newpassword})
    return str(response.status_code)


@app.route("/registerUser", methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get ('password')
    email = request.form.get('email')
    response = requests.post (authentication_url +"registerUser", data={'username': username, 'password': password, 'email': email})

    return str(response.status_code)


@app.route("/checkToken", methods=['POST'])
def checkToken():
    token = request.form.get('token')
    response = requests.post (authentication_url + "checkToken", data={'token': token})
    return str(response.status_code)

# ______________________________MAP_EDITOR_____________________________________________-

@app.route('/getMaps/<numberofPlayer>', methods=['GET'])
def getMaps(numberofPlayer):
   response= requests.get(map_editor_url +"getMaps",data={'NumberOfPlayers': numberofPlayer})
   return str(response.status_code)

@app.route('/getAllMaps', methods=['GET'])
def getAll():
   response= requests.get(map_editor_url + "getAllMaps")
   return str(response.status_code)

@app.route("/uploadMap", methods=['POST'])
def uploadMap():
    map = request.form.get('map')
    response = requests.post (map_editor_url + "uploadMap", data={'map': map})
    return str(response.status_code)

@app.route("/updateMap", methods=["PUT"])
def updateMap():
    mapid = request.args.get('mapid')
    newmapversion = request.args.get('newmapversion')
    response = requests.put (map_editor_url + "updateMap", data={'mapID': mapid,'newMapVersion': newmapversion})
    return str(response.status_code)

@app.route("/deleteMap", methods=['DELETE'])
def deleteMap():
    mapid = request.args.get('mapid')
    response = requests.delete (map_editor_url + "deleteMap", params={'mapid': mapid})
    return str(response.status_code)

# _______________________________________#Matchmaking____________________________________________

@app.route("/PutCreateGame", methods=['PUT'])
def PutCreateGame():
    UserID = request.form.get('UserID')
    response = requests.put(match_making_url +"PutCreateGame", data={'UserID': UserID})
    return str(response.status_code)

@app.route("/JoinGame", methods=['POST'])
def joinGame():
    GameID = request.form.get('GameID')
    UserID = request.form.get('UserID')
    response = requests.post(match_making_url + "JoinGame", data={'GameID': GameID,'UserID': UserID})
    return str(response.status_code)

@app.route("/PostChangeColor", methods=['POST'])
def changeColor():
    color = request.form.get('color')
    UserID = request.form.get('UserID')
    response = requests.post(match_making_url + "PostChangeColor", data={'color': color,'UserID': UserID})
    return str(response.status_code)


@app.route("/GetLobbyState", methods=['GET'])
def lobbyState():
    GameID = request.form.get('GameID')
    response = requests.get(match_making_url + "GetLobbyState", data={'GameID': GameID})
    return str(response.status_code)


@app.route("/PostAddAI1", methods=['POST'])
def addAI1():
    GameID = request.form.get('GameID')
    AIPlayerID = request.form.get('AIPlayerID')
    response = requests.post(match_making_url + "PostAddAI1", data={'GameID': GameID,'AIPlayerID': AIPlayerID})
    return str(response.status_code)

@app.route("/PostKickPlayer", methods=['POST'])
def kickPlayer():
    PlayerID = request.form.get('PlayerID')
    response = requests.post(match_making_url + "PostKickPlayer", data={'PlayerID': PlayerID})
    return str(response.status_code)

@app.route("/PostChangeHost", methods=['POST'])
def changeHost():
    GameID = request.form.get('GameID')
    response = requests.post(match_making_url + "PostChangeHost", data={'GameID': GameID})
    return str(response.status_code)

@app.route("/PostIAmReady", methods=['POST'])
def iamready():
    UserID = request.form.get('UserID')
    response = requests.post(match_making_url, data={'UserID': UserID})
    return str(response.status_code)

@app.route("/PostChangeMap", methods=['POST'])
def changeMap():
    MapID = request.form.get('MapID')
    UserID = request.form.get('UserID')
    response = requests.post(match_making_url + "PostChangeMap", data={'MapID': MapID, 'UserID': UserID})
    return str(response.status_code)


@app.route("/GetListOfGames", methods=['GET'])
def listofGames():
    response = requests.get(match_making_url)
    return str(response.status_code)

# ____________________________________Game_Engine_________________
@app.route("/PostMove", methods=['POST'])
def postMove():
    Direction = request.form.get('Direction')
    UserID = request.form.get('UserID')
    TurboFlag = request.form.get('TurboFlag')
    response = requests.post(game_engine_url + "PostMove", data={'Direction': Direction, 'UserID': UserID, 'TurboFlag':TurboFlag})

    return str(response.status_code)

@app.route("/getcurrentStateOfMOdel", methods=['GET'])
def currentState():
    GameID = request.form.get('GameID')
    response = requests.get(game_engine_url + "getcurrentStateOfMOdel", data={'GameID': GameID})
    return str(response.status_code)

@app.route("/CreateGame", methods=['POST'])
def createGame():
    GameID = request.form.get('GameID')
    ListOfUserIDs  = request.form.get('ListOfUserIDs')
    response = requests.post(game_engine_url + "CreateGame", data={'GameID': GameID,'ListOfUserIDs': ListOfUserIDs})

    return str(response.status_code)

# ____________________________leader_Boards_________________

@app.route("/RegisterNewPlayer", methods=['POST'])
def newPlayer():
    playerID = request.form.get('playerID')
    response = requests.post(scores_leader_url + "RegisterNewPlayer", data={'playerID': playerID})

    return str(response.status_code)

@app.route("/RegisterGame", methods=['POST'])
def registerGame():
    playerID = request.form.get('playerID')
    time = request.form.get('time')
    position = request.form.get('position')
    length_of_wall = request.form.get('length_of_wall')
    kills = request.form.get('kills')

    response = requests.post(scores_leader_url + "RegisterGame", data={'playerID': playerID,'time': time,'position': position,'length_of_wall': length_of_wall,'kills': kills})

    return str(response.status_code)

@app.route("/LeaderboardWins", methods=['GET'])
def leaderBoardWins():
    response = requests.get(scores_leader_url + "LeaderboardWins")
    return str(response.status_code)

@app.route("/LeaderboardTopScore", methods=['GET'])
def leaderBoardTopScore():
    response = requests.get(scores_leader_url + "LeaderboardTopScore")
    return str(response.status_code)

@app.route("/LeaderboardKills", methods=['GET'])
def leaderboardKills():
    response = requests.get(scores_leader_url + "LeaderboardKills")
    return str(response.status_code)

@app.route("/LeaderboardTimePlayed", methods=['GET'])
def leaderboardTimePlayed():
    response = requests.get(scores_leader_url + "LeaderboardTimePlayed")
    return str(response.status_code)

@app.route("/DeletePlayer", methods=['DELETE'])
def deletePlayer():
    response = requests.delete(scores_leader_url + "DeletePlayer")
    return str(response.status_code)

if __name__ == '__main__':
    app.run(debug=True)

