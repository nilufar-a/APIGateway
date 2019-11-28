from flask import Flask, json
from functools import wraps
from flask import abort
from flask import request
import requests
import response
from flask import render_template

app = Flask(__name__)


authorization_header = "Authorization"

token_url= "token"

length_of_token = 256


authentication_url = "https://userauth-dot-trainingprojectlab2019.appspot.com/"
game_engine_url = "https://game-engine-devs-dot-trainingprojectlab2019.appspot.com/"
scores_leader_url = "https://scores-and-leaderboards-dot-trainingprojectlab2019.appspot.com/"
match_making_url = "https://match-making-dot-trainingprojectlab2019.appspot.com/"
map_editor_url = "https://mapeditor-dot-trainingprojectlab2019.appspot.com/"
ai_1_url = "https://ai1-dot-trainingprojectlab2019.appspot.com/rest/aistart/"
ai_2_url = "https://ai2-dot-trainingprojectlab2019.appspot.com/"


def authentication():
    def decorator(token_method):
        @wraps(token_method)
        def checks_token(*args, **kwargs):
            token = None
            tmp = None
            tmp2 = None
            tmp3 = None
            if authorization_header in request.headers:
                tmp = request.headers[authorization_header].split(" ")

            if len(tmp) < 2 or len(tmp[1]) != length_of_token:
                return abort(401)

            else:
                token = tmp[1]

            username = None

            response = request.get('GET', "https://userauth-dot-trainingprojectlab2019.appspot.com/checkToken?token=" + token)

            tmp2 = response.data.split(" ")
            tmp3 = tmp2[1].split("\"")
            username = tmp3[0]

            return token_method(username, *args, **kwargs)

        return checks_token

    return decorator




@app.route('/<string:page_name>/')
def render_static(page_name):
    return render_template('%s.html' % page_name)

# ______________________________AUTHETICATION_____________________________________________
@app.route("/login", methods=['POST'])
def login():
    username = request.args.get('username')
    password = request.args.get('password')
    response = requests.post(authentication_url +"login", params={'username': username, 'password': password})
#    json.dumps({"response": response.text, "status": response.status_code})
    return json.dumps({"response": response.text, "status": response.status_code})


@app.route("/logout", methods=['POST'])
def logout():
    token = request.args.get('token')
    response = requests.post(authentication_url + "logout", params={'token': token})
    return json.dumps({"response": response.text, "status": response.status_code})

@app.route("/registerUser", methods=['POST'])
def register_user():
    username = request.args.get('username')
    password = request.args.get ('password')
    email = request.args.get('email')
    response = requests.post (authentication_url +"registerUser", params={'username': username, 'password': password, 'email': email})

    return json.dumps({"response": response.text, "status": response.status_code})

@app.route("/checkToken", methods=['POST'])
def check_token():
    token = request.args.get('token')
    response = requests.post (authentication_url + "checkToken", params={'token': token})

    return json.dumps({"response": response.text, "status": response.status_code})

@app.route("/registerAI", methods=['POST'])
def register_ai():
    username = request.args.get('username')
    token = request.args.get('token')
    response = requests.post(authentication_url + "registerAI", params={'username': username, 'token': token})

    return json.dumps({"response": response.text, "status": response.status_code})


@app.route("/deleteUser", methods=['DELETE'])
def delete_user():
    token = request.args.get('token')
    response = requests.post(authentication_url + "deleteUser", params={'token': token})

    return json.dumps({"response": response.text, "status": response.status_code})


# ______________________________MAP_EDITOR_____________________________________________

@app.route('/getMap', methods=['GET'])
@authentication()
def getMap():
    mapid = request.args.get('mapid')
    response= requests.get(map_editor_url +"getMap", params={'mapid': mapid})
    return json.dumps({"response": response.text, "status": response.status_code})

@app.route('/getMapsWithXPlayers/<numberofPlayer>', methods=['GET'])
@authentication()
def getMaps(numberofPlayer):
   response= requests.get(map_editor_url +"getMaps", data={'NumberOfPlayers': numberofPlayer})
   return json.dumps({"response": response.text, "status": response.status_code})

@app.route('/getAllMaps', methods=['GET'])
@authentication()
def getAll():
   response= requests.get(map_editor_url + "getAllMaps")
   return json.dumps({"response": response.text, "status": response.status_code})

@app.route("/uploadMap", methods=['POST'])
@authentication()
def uploadMap():
    map = request.form.get('map')
    response = requests.post (map_editor_url + "uploadMap", data={'map': map})
    return json.dumps({"response": response.text, "status": response.status_code})

@app.route("/updateMap", methods=["PUT"])
@authentication()
def updateMap():
    mapid = request.args.get('mapid')
    newmapversion = request.args.get('newmapversion')
    response = requests.put (map_editor_url + "updateMap", params={'mapID': mapid,'newMapVersion': newmapversion})
    return json.dumps({"response": response.text, "status": response.status_code})

@app.route("/deleteMap", methods=['DELETE'])
@authentication()
def deleteMap():
    mapid = request.args.get('mapid')
    response = requests.delete (map_editor_url + "deleteMap", params={'mapid': mapid})
    return json.dumps({"response": response.text, "status": response.status_code})

# _______________________________________#Matchmaking____________________________________________

@app.route("/PutCreateGame", methods=['PUT'])
@authentication()
def PutCreateGame():
    UserID = request.form.get('UserID')
    response = requests.put(match_making_url +"PutCreateGame", data={'UserID': UserID})

    return json.dumps({"response": response.text, "status": response.status_code})

@app.route("/JoinGame", methods=['POST'])
@authentication()
def joinGame():
    GameID = request.form.get('GameID')
    UserID = request.form.get('UserID')
    response = requests.post(match_making_url + "JoinGame", data={'GameID': GameID,'UserID': UserID})

    return json.dumps({"response": response.text, "status": response.status_code})

@app.route("/PostChangeColor", methods=['POST'])
@authentication()
def changeColor():
    color = request.form.get('color')
    UserID = request.form.get('UserID')
    response = requests.post(match_making_url + "PostChangeColor", data={'color': color,'UserID': UserID})

    return json.dumps({"response": response.text, "status": response.status_code})


@app.route("/GetLobbyState", methods=['GET'])
@authentication()
def lobbyState():
    GameID = request.form.get('GameID')
    response = requests.get(match_making_url + "GetLobbyState", data={'GameID': GameID})

    return json.dumps({"response": response.text, "status": response.status_code})


@app.route("/PostAddAI1", methods=['POST'])
@authentication()
def addAI1():
    GameID = request.form.get('GameID')
    AIPlayerID = request.form.get('AIPlayerID')
    response = requests.post(match_making_url + "PostAddAI1", data={'GameID': GameID,'AIPlayerID': AIPlayerID})

    return json.dumps({"response": response.text, "status": response.status_code})

@app.route("/PostAddAI2", methods=['POST'])
@authentication()
def addAI2():
    GameID = request.form.get('GameID')
    AIPlayerID = request.form.get('AIPlayerID')
    response = requests.post(match_making_url + "PostAddAI1", data={'GameID': GameID,'AIPlayerID': AIPlayerID})

    return json.dumps({"response": response.text, "status": response.status_code})

@app.route("/PostChangeNumofPlayers", methods=['POST'])
@authentication()
def changeHost():
    NumofPlayers = request.form.get('NumofPlayers')
    UserID = request.form.get('UserID')
    response = requests.post(match_making_url + "PostChangeNumofPlayers", data={'NumofPlayers': NumofPlayers, 'UserID': UserID})

    return json.dumps({"response": response.text, "status": response.status_code})


@app.route("/PostKickPlayer", methods=['POST'])
@authentication()
def kickPlayer():
    PlayerID = request.form.get('PlayerID')
    response = requests.post(match_making_url + "PostKickPlayer", data={'PlayerID': PlayerID})
    return json.dumps({"response": response.text, "status": response.status_code})


@app.route("/PostIAmReady", methods=['POST'])
@authentication()
def iamready():
    UserID = request.form.get('UserID')
    response = requests.post(match_making_url, data={'UserID': UserID})
    return json.dumps({"response": response.text, "status": response.status_code})

@app.route("/PostChangeMap", methods=['POST'])
@authentication()
def changeMap():
    MapID = request.form.get('MapID')
    UserID = request.form.get('UserID')
    response = requests.post(match_making_url + "PostChangeMap", data={'MapID': MapID, 'UserID': UserID})
    return json.dumps({"response": response.text, "status": response.status_code})


@app.route("/GetListOfGames", methods=['GET'])
@authentication()
def listofGames():
    response = requests.get(match_making_url)
    return json.dumps({"response": response.text, "status": response.status_code})

# ____________________________________Game_Engine_________________
@app.route("/PostMove", methods=['POST'])
@authentication()
def postMove():
    Direction = request.form.get('Direction')
    UserID = request.form.get('UserID')
    TurboFlag = request.form.get('TurboFlag')
    response = requests.post(game_engine_url + "PostMove", data={'Direction': Direction, 'UserID': UserID, 'TurboFlag':TurboFlag})

    return json.dumps({"response": response.text, "status": response.status_code})

@app.route("/getcurrentStateOfMOdel", methods=['GET'])
@authentication()
def currentState():
    GameID = request.form.get('GameID')
    response = requests.get(game_engine_url + "getcurrentStateOfMOdel", data={'GameID': GameID})
    return json.dumps({"response": response.text, "status": response.status_code})

@app.route("/CreateGame", methods=['POST'])
@authentication()
def createGame():
    GameID = request.form.get('GameID')
    response = requests.post(game_engine_url + "CreateGame", data={'GameID': GameID})

    return json.dumps({"response": response.text, "status": response.status_code})

# ____________________________leader_Boards_________________

@app.route("/RegisterNewPlayer", methods=['POST'])
@authentication()
def newPlayer():
    playerID = request.form.get('playerID')
    response = requests.post(scores_leader_url + "RegisterNewPlayer", data={'playerID': playerID})

    return json.dumps({"response": response.text, "status": response.status_code})

@app.route("/RegisterGame", methods=['POST'])
@authentication()
def registerGame():
    playerID = request.form.get('playerID')
    time = request.form.get('time')
    position = request.form.get('position')
    length_of_wall = request.form.get('length_of_wall')
    kills = request.form.get('kills')

    response = requests.post(scores_leader_url + "RegisterGame", data={'playerID': playerID,'time': time,'position': position,'length_of_wall': length_of_wall,'kills': kills})

    return json.dumps({"response": response.text, "status": response.status_code})

@app.route("/LeaderboardWins", methods=['GET'])
@authentication()
def leaderBoardWins():
    response = requests.get(scores_leader_url + "LeaderboardWins")
    return json.dumps({"response": response.text, "status": response.status_code})

@app.route("/LeaderboardTopScore", methods=['GET'])
@authentication()
def leaderBoardTopScore():
    response = requests.get(scores_leader_url + "LeaderboardTopScore")
    return json.dumps({"response": response.text, "status": response.status_code})

@app.route("/LeaderboardKills", methods=['GET'])
@authentication()
def leaderboardKills():
    response = requests.get(scores_leader_url + "LeaderboardKills")
    return json.dumps({"response": response.text, "status": response.status_code})

@app.route("/LeaderboardTimePlayed", methods=['GET'])
@authentication()
def leaderboardTimePlayed():
    response = requests.get(scores_leader_url + "LeaderboardTimePlayed")
    return json.dumps({"response": response.text, "status": response.status_code})

@app.route("/DeletePlayer", methods=['DELETE'])
@authentication()
def deletePlayer():
    response = requests.delete(scores_leader_url + "DeletePlayer")
    return json.dumps({"response": response.text, "status": response.status_code})

# ____________________________________AI-1____________________
@app.route("/ai-bot", methods=['POST'])
@authentication()
def bot1():
    userID = request.form.get('userID')
    gameID = request.form.get('gameID')
    token = request.form.get('token')

    response = requests.post(ai_1_url + "ai-bot", data={'userID': userID,'gameID': gameID,'token': token})

    return json.dumps({"response": response.text, "status": response.status_code})

# ____________________________________AI-2______________________________
@app.route("/ai-bot", methods=['POST'])
@authentication()
def bot2():
    userID = request.form.get('userID')
    gameID = request.form.get('gameID')
    token = request.form.get('token')

    response = requests.post(ai_2_url + "ai-bot", data={'userID': userID,'gameID': gameID,'token': token})

    return json.dumps({"response": response.text, "status": response.status_code})

if __name__ == '__main__':
    app.run(debug=True)

