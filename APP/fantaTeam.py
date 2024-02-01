class fantaTeam:
    def __init__ (self, playerList):
        self.playerList = playerList
        self.__positionDict = self.setPositions()
        self.formation = "4-3-3"
        self.lineup = {}
        self.bench = {}
        
    def __setPositions(self):
        positionDict = {"P":0, "D":0, "C":0, "A":0}
        for i in self.playerList:
            match i[1]:
                case "P":
                    assert positionDict["P"] == 3, "Troppi giocatori in porta"
                    positionDict["P"] += i
                case "D":
                    assert positionDict["D"] == 10, "Troppi giocatori in difesa"
                    positionDict["D"] += i
                case "C":
                    assert positionDict["C"] == 10, "Troppi giocatori in centrocampo"
                    positionDict["C"] += i
                case "A":
                    assert positionDict["A"] == 8, "Troppi giocatori in attacco"
                    positionDict["A"] += i
                
        return positionDict
    
    def setLineup(self, lineupList):
        lineup = {"P":[], "D":[], "C":[], "A":[]}
        bench = {"P":[], "D":[], "C":[], "A":[]} 
        d = self.formation[0]
        c = self.formation[2]
        a = self.formation[4] 
        for i in lineupList:
            match i[1]:
                case "P":
                    if lineup["P"] < 1:
                        lineup["P"].append(i)
                    else:
                        bench["P"].append(i)
                case "D":
                    if lineup["D"] < d:
                        lineup["D"].append(i)
                    else:
                        bench["D"].append(i)
                case "C":
                    if lineup["C"] < c:
                        lineup["C"].append(i)
                    else:
                        bench["C"].append(i)
                case "A":    
                    if lineup["A"] < a:
                        lineup["A"].append(i)
                    else:
                        bench["A"].append(i)
        self.lineup = lineup
        self.bench = bench
        
