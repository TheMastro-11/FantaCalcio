import matchStats
import tournamentStats


round = tournamentStats.TournamentStats(22)
roundDict = {}
for i in round.matches:
    match = matchStats.MatchStats(round.matches[i][2]) #genero nuova partita
    match.getRating()
    match.getEvents()   
    roundDict[i] = match.teamDict


print(roundDict)