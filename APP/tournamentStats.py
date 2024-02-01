import requests
from datetime import datetime
import json

class TournamentStats:
    def __init__(self,roundId):
        self.roundId = roundId
        self.__url = "https://sofascore.p.rapidapi.com/tournaments/get-last-matches"
        self.__querystring = {"tournamentId":"23","seasonId":"52760","pageIndex":"0"}
        self.__headers = {
            "X-RapidAPI-Key": "754fb3dd1cmsh3db675bb2c05431p134a9fjsn928a5567ea5c",
            "X-RapidAPI-Host": "sofascore.p.rapidapi.com"
        }
        self.__response = json.load(open("/Users/mastro/Documents/GitHub/FantaCalcio/APP/JSON/round.json"))#requests.get(self.__url, headers=self.__headers, params=self.__querystring)
        self.matches = self.getMatches()
        
    def getMatches(self):
        matches = {}
    
        for i in self.__response["events"]: #.json()
            if i["roundInfo"]["round"] == self.roundId:
                time = i["startTimestamp"]
                dateTime = datetime.fromtimestamp(time)
                matches[i["homeTeam"]["name"] + " - " + i["awayTeam"]["name"]] = [dateTime.strftime("%d-%b-%Y (%H:%M)"), str(i["homeScore"]["current"]) + "-" + str(i["awayScore"]["current"]), i["id"]]
        return matches
    
   