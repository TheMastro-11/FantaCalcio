import requests
from datetime import datetime

class TournamentStats:
    def __init__(self,roundId):
        self.roundId = roundId
        self.url = "https://sofascore.p.rapidapi.com/tournaments/get-last-matches"
        self.querystring = {"tournamentId":"23","seasonId":"52760","pageIndex":"0"}
        self.headers = {
            "X-RapidAPI-Key": "754fb3dd1cmsh3db675bb2c05431p134a9fjsn928a5567ea5c",
            "X-RapidAPI-Host": "sofascore.p.rapidapi.com"
        }
        self.response = requests.get(self.url, headers=self.headers, params=self.querystring)
        self.matches = self.getMatches()
        
    def getMatches(self):
        matches = {}
    
        for i in self.response.json()["events"]:
            if i["roundInfo"]["round"] == self.roundId:
                time = i["startTimestamp"]
                dateTime = datetime.fromtimestamp(time)
                matches[i["homeTeam"]["name"] + " - " + i["awayTeam"]["name"]] = [dateTime.strftime("%d-%b-%Y (%H:%M)"), str(i["homeScore"]["current"]) + "-" + str(i["awayScore"]["current"])]
        return matches
    
    