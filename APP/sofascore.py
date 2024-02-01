import matchStats
import tournamentStats


round = tournamentStats.TournamentStats(22)
roundDict = {}
for i in round.matches: #i = nome singola partita
    match = matchStats.MatchStats(round.matches[i][2], i) #genero nuova partita
    match.getStats() 
    roundDict[i] = match.teamDict #punteggio giocatori


for i in roundDict: #per ogni partita
    print( i, "\n") #nome partita
    for j in roundDict[i]:#per ogni giocatore 
        print(j, roundDict[i][j]) #nome giocatore, punteggio giocatore
