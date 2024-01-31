import requests

class MatchStats:
    def __init__(self, matchId):
        self.matchId = matchId
        self.url = "https://sofascore.p.rapidapi.com/matches/get-lineups" #formazioni
        self.url2 = "https://sofascore.p.rapidapi.com/matches/get-incidents" #eventi
        self.querystring = {"matchId": self.matchId} #codice partita
        self.headers = {
            "X-RapidAPI-Key": "754fb3dd1cmsh3db675bb2c05431p134a9fjsn928a5567ea5c",
            "X-RapidAPI-Host": "sofascore.p.rapidapi.com"
        }
        self.lineupsResponse = requests.get(self.url, headers=self.headers, params=self.querystring)
        self.incidentResponse = requests.get(self.url2, headers=self.headers, params=self.querystring)
        self.lineups = self.lineupsResponse.json()
        self.incidents = self.incidentResponse.json()["incidents"]
        self.homeTeam = self.lineups["home"]["players"]
        self.awayTeam = self.lineups["away"]["players"]
        self.teamDict = self.getTeam()
    
    def arrotonda(self, num):
        if num%0.5 >= 0.25:
            return num-num%0.5+0.5
        return num-num%0.5
    
    def getTeam(self):
        teamDict = {}
        #salvo i giocatori
        for i in self.homeTeam:
            teamDict[i["player"]["name"]] = []
        for i in self.awayTeam:
            teamDict[i["player"]["name"]] = []
        return teamDict 
            
    def getRating(self):
        #salvo i voti dei giocatori
        for i in self.homeTeam:
            if i["statistics"] != {} and "rating" in i["statistics"]:
                rate = self.arrotonda(i["statistics"]["rating"]) #pagella
                fv = rate #fantaVoto
                self.teamDict[i["player"]["name"]] = [rate,fv]

        for i in self.awayTeam:
            if i["statistics"] != {} and "rating" in i["statistics"]:
                rate = self.arrotonda(i["statistics"]["rating"]) #pagella
                fv = rate #fantaVoto
                self.teamDict[i["player"]["name"]] = [rate,fv]
                
    def getEvents(self):
        #salvo eventi
        for i in self.incidents:
            if i["incidentType"] == "card": #cartellini
                if "player" in i:
                    self.teamDict[i["player"]["name"]].append(i["incidentClass"])
                    if i["incidentClass"] == "yellow":
                        self.teamDict[i["player"]["name"]][1] = self.teamDict[i["player"]["name"]][1] - 0.5
                    elif i["incidentClass"] == "red":
                        self.teamDict[i["player"]["name"]][1] = self.teamDict[i["player"]["name"]][1] - 1
            if i["incidentType"] == "goal": #gol
                self.teamDict[i["player"]["name"]].append(i["incidentType"])
                self.teamDict[i["player"]["name"]][1] = self.teamDict[i["player"]["name"]][1] + 3
            if i["incidentType"] == "substitution": #sostituzioni
                self.teamDict[i["playerIn"]["name"]].append(i["incidentType"] + " in at " + str(i["time"]))
                self.teamDict[i["playerOut"]["name"]].append(i["incidentType"] + " out at " + str(i["time"]))