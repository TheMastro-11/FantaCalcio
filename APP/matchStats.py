import requests
import json

class MatchStats:
    def __init__(self, matchId, matchName):
        self.matchId = matchId
        self.matchName = matchName
        self.__url = "https://sofascore.p.rapidapi.com/matches/get-lineups" #formazioni
        self.__url2 = "https://sofascore.p.rapidapi.com/matches/get-incidents" #eventi
        self.__querystring = {"matchId": self.matchId} #codice partita
        self.__headers = {
            "X-RapidAPI-Key": "754fb3dd1cmsh3db675bb2c05431p134a9fjsn928a5567ea5c",
            "X-RapidAPI-Host": "sofascore.p.rapidapi.com"
        }
        self.__lineupsResponse = json.load(open("/Users/mastro/Documents/GitHub/FantaCalcio/APP/JSON/"+ self.matchName +"Lineups.json"))#requests.get(self.__url, headers=self.__headers, params=self.__querystring)
        self.__incidentResponse = json.load(open("/Users/mastro/Documents/GitHub/FantaCalcio/APP/JSON/"+ self.matchName +"Incidents.json"))#requests.get(self.__url2, headers=self.__headers, params=self.__querystring)
        self.__lineups = self.__lineupsResponse#.json()
        self.__incidents = self.__incidentResponse#.json()["incidents"]
        self.__homeTeam = self.__lineups["home"]["players"]
        self.__awayTeam = self.__lineups["away"]["players"]
        self.__currentHomeKeeper = ""
        self.__currentAwayKeeper = ""
        self.teamDict = self.__getTeam()
    
    def __arrotonda(self, num):
        if num%0.5 >= 0.25:
            return num-num%0.5+0.5
        return num-num%0.5
    
    def __getTeam(self):
        teamDict = {}
        #salvo i giocatori
        self.__currentHomeKeeper = self.__homeTeam[0]["player"]["name"] #portiere
        for i in self.__homeTeam:
            teamDict[i["player"]["name"]] = []
            
        self.__currentAwayKeeper = self.__awayTeam[0]["player"]["name"] #portiere
        for i in self.__awayTeam:
            teamDict[i["player"]["name"]] = []
        
        return teamDict 
            
    def __getRating(self):
        #salvo i voti dei giocatori
        for i in self.__homeTeam:
            if i["statistics"] != {} and "rating" in i["statistics"]:
                rate = self.__arrotonda(i["statistics"]["rating"]) #pagella
                fv = rate #fantaVoto
                self.teamDict[i["player"]["name"]] = [rate,fv]

        for i in self.__awayTeam:
            if i["statistics"] != {} and "rating" in i["statistics"]:
                rate = self.__arrotonda(i["statistics"]["rating"]) #pagella
                fv = rate #fantaVoto
                self.teamDict[i["player"]["name"]] = [rate,fv]
                
    def __getEvents(self):
        #salvo eventi
        for i in reversed(self.__incidents):
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
                for k in self.__homeTeam:
                    if k["player"]["name"] == i["player"]["name"]:
                        self.teamDict[self.__currentAwayKeeper].append("goal against")
                        self.teamDict[self.__currentAwayKeeper][1] = self.teamDict[self.__currentAwayKeeper][1] - 1  
                for j in self.__awayTeam:
                    if j["player"]["name"] == i["player"]["name"]: #segno un gol al portiere avversario
                        self.teamDict[self.__currentHomeKeeper].append("goal against")
                        self.teamDict[self.__currentHomeKeeper][1] = self.teamDict[self.__currentHomeKeeper][1] - 1
                        
                    
            if i["incidentType"] == "substitution": #sostituzioni
                if i["playerOut"]["name"] == self.__currentHomeKeeper:
                    self.__currentHomeKeeper = i["playerIn"]["name"]
                if i["playerOut"]["name"] == self.__currentAwayKeeper:
                    self.__currentAwayKeeper = i["playerIn"]["name"]
                self.teamDict[i["playerIn"]["name"]].append(i["incidentType"] + " in at " + str(i["time"]))
                self.teamDict[i["playerOut"]["name"]].append(i["incidentType"] + " out at " + str(i["time"]))
            
            if i["incidentType"] == "inGamePenalty":
                self.teamDict[i["player"]["name"]].append(i["incidentType"])
                if i["incidentClass"] == "missed":
                    self.teamDict[i["player"]["name"]].append("penalty missed")
                    self.teamDict[i["player"]["name"]][1] = self.teamDict[i["player"]["name"]][1] - 3 #tolgo tre punti al giocatore
                    if i["reason"] == "goalkeeperSave":
                        for k in self.__homeTeam:
                            if k["player"]["name"] == i["player"]["name"]:
                                self.teamDict[self.__currentAwayKeeper].append("penalty saved")
                                self.teamDict[self.__currentAwayKeeper][1] = self.teamDict[self.__currentAwayKeeper][1] + 3
                        for j in self.__awayTeam:
                            if j["player"]["name"] == i["player"]["name"]: #aggiungo tre punti al portiere avversario
                                self.teamDict[self.__currentHomeKeeper].append("penalty saved")
                                self.teamDict[self.__currentHomeKeeper][1] = self.teamDict[self.__currentHomeKeeper][1] + 3
                            
                else: #aggiungo tre punti al giocatore
                    self.teamDict[i["player"]["name"]].append("penalty scored")
                    self.teamDict[i["player"]["name"]][1] = self.teamDict[i["player"]["name"]][1] + 3
                                    
        #verifico imbattibilità portiere
        if "goal against" not in self.teamDict[self.__currentHomeKeeper]:
            self.teamDict[self.__currentHomeKeeper].append("clean sheet")
            self.teamDict[self.__currentHomeKeeper][1] = self.teamDict[self.__currentHomeKeeper][1] + 1
        if "goal against" not in self.teamDict[self.__currentAwayKeeper]:
            self.teamDict[self.__currentAwayKeeper].append("clean sheet")
            self.teamDict[self.__currentAwayKeeper][1] = self.teamDict[self.__currentAwayKeeper][1] + 1
                
                
    def getStats(self):
        self.__getRating()
        self.__getEvents()
        return self.teamDict
    
    