from flask import Flask, json, render_template
from flask import request
import requests


authentication_url = "https://userauth-dot-trainingprojectlab2019.appspot.com/"
scores_leader_url = "https://scores-and-leaderboards-dot-trainingprojectlab2019.appspot.com/"
map_editor_url = "https://mapeditor-dot-trainingprojectlab2019.appspot.com/"
game_engine_url = "https://game-engine-devs-dot-trainingprojectlab2019.appspot.com/"
match_making_url = "https://match-making-dot-trainingprojectlab2019.appspot.com/"
ai_1_url = "https://ai1-dot-trainingprojectlab2019.appspot.com/"
ai_2_url = "https://ai2-dot-trainingprojectlab2019.appspot.com/"

app = Flask(__name__)
@app.route("/", methods=['GET'])
def hello():
    return "This is our game"


@app.route('/<string:page_name>/')
def render_static(page_name):
    return render_template('%s.html' % page_name)

# ______________________________AUTHENTICATION_____________________________________________
@app.route("/login", methods=['POST'])
def login():
    username = request.args.get('username')
    password = request.args.get('password')
    response = requests.post(authentication_url +"login", params={'username': username, 'password': password})
    return json.dumps({"response": response.json(), "status": response.status_code})

@app.route("/logout", methods=['POST'])
def logout():
    token = request.args.get('token')
    response = requests.post(authentication_url + "logout", params={'token': token})
    return json.dumps({"response": response.json(), "status": response.status_code})

@app.route("/register", methods=['POST'])
def register_user():
    username = request.args.get('username')
    password = request.args.get ('password')
    email = request.args.get('email')
    response = requests.post (authentication_url +"registerUser", params={'username': username, 'password': password, 'email': email})

    return json.dumps({"response": response.json(), "status": response.status_code})

@app.route("/checktoken", methods=['GET'])
def check_token():
    token = request.args.get('token')
    response = requests.get (authentication_url + "checktoken", params={'token': token})

    return json.dumps({"response": response.json(), "status": response.status_code})

@app.route("/registerai", methods=['POST'])
def register_ai():
    username = request.args.get('username')
    token = request.args.get('token')
    response = requests.post(authentication_url + "registerAI", params={'username': username, 'token': token})

    return json.dumps({"response": response.json(), "status": response.status_code})


@app.route("/deleteuser", methods=['DELETE'])
def delete_user():
    token = request.args.get('token')
    response = requests.delete(authentication_url + "deleteUser", params={'token': token})

    return json.dumps({"response": response.json(), "status": response.status_code})

# ______________________________ScoresandLeaderboards_____________________________________________
@app.route("/RegisterGame", methods=['POST'])
def registerGame():
    userID = request.args.get('userID')
    score = request.args.get('score')
    wins = request.args.get('wins')
    kills = request.args.get('kills')
    timePlayed = request.args.get('timePlayed')
    response = requests.post(scores_leader_url + "RegisterGame", params={'userID': userID, 'score': score,'wins': wins, 'kills': kills, 'timePlayed': timePlayed})

    return json.dumps({"response": response.text, "status": response.status_code})

@app.route("/GetLeaderBoardX", methods=['GET'])
def getLeaderBoardX():
    boardName = request.args.get('boardName')
    response = requests.get(scores_leader_url + "GetLeaderBoardX",params={'boardName': boardName})

    return json.dumps({"response": response.text, "status": response.status_code})

@app.route("/DeleteScore", methods=['DELETE'])
def delete_score():
    userID = request.args.get('userID')
    response = requests.delete(scores_leader_url + "DeleteScore", params={'userID': userID})

    return json.dumps({"response": response.text, "status": response.status_code})

# ______________________________MAP_EDITOR_____________________________________________

@app.route('/getMap', methods=['GET'])
def getMap():
    name = request.args.get('name')
    response= requests.get(map_editor_url +"getMap", params={'name': name})
    return json.dumps({"response":response.json(), "status": response.status_code})

@app.route('/getMapsWithXPlayers/<NumberofPlayers>', methods=['GET'])
def getMapsWithXPlayers(NumberofPlayers):
   response= requests.get(map_editor_url +"getMaps", params={'NumberOfPlayers': NumberofPlayers})
   return json.dumps({"response": response.text, "status": response.status_code})

@app.route('/isNameOccupied', methods=['GET'])
def isNameOccupied():
    name = request.args.get('name')
    response = requests.get(map_editor_url + "isNameOccupied", params={'name': name})
    return json.dumps({"response": response.text, "status": response.status_code})
@app.route('/getAllMaps', methods=['GET'])
def getAllMaps():
   response= requests.get(map_editor_url + "getAllMaps")
   return json.dumps({"response": response.text, "status": response.status_code})

@app.route("/uploadMap", methods=['POST'])
def uploadMap():
    map = request.args.get('map')
    response = requests.post (map_editor_url + "uploadMap", params={'map': map})
    return json.dumps({"response": response.text, "status": response.status_code})

@app.route("/updateMap", methods=["PUT"])
def updateMap():
    name = request.args.get('name')
    newmapversion = request.args.get('newmapversion')
    response = requests.put (map_editor_url + "updateMap", params={'name': name,'newMapVersion': newmapversion})
    return json.dumps({"response": response.text, "status": response.status_code})

@app.route("/deleteMap", methods=['DELETE'])
def deleteMap():
    name = request.args.get('name')
    response = requests.delete (map_editor_url + "deleteMap", params={'name': name})
    return json.dumps({"response": response.text, "status": response.status_code})
# ____________________________________Game_Engine_________________
@app.route("/PostMove", methods=['POST'])
def postMove():
    Direction = request.args.get('Direction')
    UserID = request.args.get('UserID')
    TurboFlag = request.args.get('TurboFlag')
    response = requests.post(game_engine_url + "PostMove", params={'Direction': Direction, 'UserID': UserID, 'TurboFlag':TurboFlag})

    return json.dumps({"response": response.text, "status": response.status_code})

@app.route("/GetCurrentStateOfModel", methods=['GET'])
def currentState():
    GameID = request.args.get('GameID')
    response = requests.get(game_engine_url + "getcurrentStateOfMOdel", params={'GameID': GameID})
    return json.dumps({"response": response.text, "status": response.status_code})

@app.route("/PostCreateGame", methods=['POST'])
def createGame():
    GameID = request.args.get('GameID')
    response = requests.post(game_engine_url + "PostCreateGame", params={'GameID': GameID})

    return json.dumps({"response": response.text, "status": response.status_code})
# ____________________________________Matchmaking____________________
@app.route("/PutCreateGame", methods=['PUT'])
def putcreategame():
    UserID = request.args.get('userID')
    response = requests.put(match_making_url + "PutCreateGame", params={'UserID': UserID})

    return json.dumps({"response": response.text, "status": response.status_code})
@app.route("/JoinGame", methods=['POST'])
def joingame():
    GameID = request.args.get('GameID')
    UserID = request.args.get('userID')
    response = requests.post(match_making_url + "JoinGame", params={'GameID': GameID,'UserID': UserID})

    return json.dumps({"response": response.text, "status": response.status_code})

@app.route("/PostChangeColor", methods=['POST'])
def changecolor():
    color = request.args.get('color')
    UserID = request.args.get('userID')
    response = requests.post(match_making_url + "PostChangeColor", params={'color': color,'UserID': UserID})

    return json.dumps({"response": response.text, "status": response.status_code})

@app.route("/GetLobbyState", methods=['GET'])
def lobbystate():
    GameID = request.args.get('GameID')
    response = requests.get(match_making_url + "GetLobbyState", params={'GameID': GameID})

    return json.dumps({"response": response.text, "status": response.status_code})


@app.route("/PostAddAI1", methods=['POST'])
def addai1():
    GameID = request.args.get('GameID')
    AIPlayerID = request.args.get('AIPlayerID')
    response = requests.post(match_making_url + "PostAddAI1", params={'GameID': GameID,'AIPlayerID': AIPlayerID})

    return json.dumps({"response": response.text, "status": response.status_code})

@app.route("/PostAddAI2", methods=['POST'])
def addai2():
    GameID = request.args.get('GameID')
    AIPlayerID = request.args.get('AIPlayerID')
    response = requests.post(match_making_url + "PostAddAI2", params={'GameID': GameID,'AIPlayerID': AIPlayerID})
    return json.dumps({"response": response.text, "status": response.status_code})


@app.route("/PostChangeNumofPlayers", methods=['POST'])
def changenumplayer():
    NumofPlayers = request.args.get('NumofPlayers')
    UserID = request.args.get('userID')
    response = requests.post(match_making_url + "PostChangeNumofPlayers", params={'NumofPlayers': NumofPlayers,'UserID': UserID})

    return json.dumps({"response": response.text, "status": response.status_code})

@app.route("/PostChangeTurnInterval", methods=['POST'])
def changeturn():
    UserID = request.args.get('userID')
    turnInterval = request.args.get('turnInterval')
    response = requests.post(match_making_url + "PostChangeTurnInterval", params={'UserID': UserID,'turnInterval': turnInterval})

    return json.dumps({"response": response.text, "status": response.status_code})

@app.route("/PostChangeCycleBehaviour", methods=['POST'])
def cycle():
    UserID = request.args.get('userID')
    disappear = request.args.get('disappear')
    response = requests.post(match_making_url + "PostChangeCycleBehaviour", params={'UserID': UserID,'disappear': disappear})

    return json.dumps({"response": response.text, "status": response.status_code})

@app.route("/PostKickPlayer", methods=['POST'])
def kickplayer():
    PlayerID = request.args.get('PlayerID')
    response = requests.post(match_making_url + "PostKickPlayer", params={'PlayerID': PlayerID})

    return json.dumps({"response": response.text, "status": response.status_code})

@app.route("/PostIAmReady", methods=['POST'])
def iamready():
    UserID = request.args.get('UserID')
    response = requests.post(match_making_url + "PostIAmReady", params={'UserID': UserID})

    return json.dumps({"response": response.text, "status": response.status_code})

@app.route("/PostChangeMap", methods=['POST'])
def changemap():
    MapID = request.args.get('MapID')
    UserID = request.args.get('UserID')
    response = requests.post(match_making_url + "PostChangeMap", params={'MapID': MapID,'UserID': UserID})

    return json.dumps({"response": response.text, "status": response.status_code})

@app.route("/GetListOfGames", methods=['GET'])
def getlist():
    response = requests.get(match_making_url + "GetListOfGames")

    return json.dumps({"response": response.text, "status": response.status_code})

# ____________________________________AI-1____________________
@app.route("/ai-bot-1", methods=['POST'])
def bot1():
    userID = request.form.get('userID')
    gameID = request.form.get('gameID')
    token = request.form.get('token')
    response = requests.post(ai_1_url + "ai-bot", json={'userID': userID,'gameID': gameID,'token': token})
    return json.dumps({"response": response.json(),"status": response.status_code})

# ____________________________________AI-2______________________________
@app.route("/ai-bot-2", methods=['POST'])
def bot2():
    userID = request.form.get('userID')
    gameID = request.form.get('gameID')
    token = request.form.get('token')
    response = requests.post(ai_1_url + "ai-bot", json={'userID': userID, 'gameID': gameID, 'token': token})
    return json.dumps({"response": response.json(), "status": response.status_code})
