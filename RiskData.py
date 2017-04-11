#! python3

import random
import logging
import RiskRaw
from RiskRaw import *

#set logging: default is WARNING
#change to INFO to see more update output
logging.basicConfig(level=logging.WARNING)
 
class Territory():

    def __init__(self, number):
        self.number = number
        self.owner = None
        self.units = None
        if self.number != None:
            self.RGB = (self.number, 150, 100)
            self.touch = touching[self.number]
            self.coord = coordinates[self.number]
            if self.number in altCoordinates:
                self.alt = altCoordinates[self.number]
            else:
                self.alt = None

    #overload repr to see territory stats for debugging
    def __repr__(self):
        return ("Terr: "+str(self.number)+", owner: "+str(self.owner)+
                ", units: "+str(self.units)+", starting RGB: "+str(self.RGB))

#colors arrays for setting initial color/bright
colors = [red, blue, yellow, green, orange, purple]
brights = [brightRed, brightBlue, brightYellow, brightGreen, brightOrange, brightPurple]

class Player():

    #def __init__(self, number): #, name, color):
    def __init__(self, number, name=""): #, color):
        self.number = number
        #self.name = ("Player " +str(self.number))
        if name == "":
            self.name = ("Player " +str(self.number+1))
        else:
            self.name = name
        self.color = colors[self.number]
        self.bright = brights[self.number]
        self.units = 0
        self.terr = 0
        self.cards = 0

    #overload repr to see player stats for debugging
    def __repr__(self):
        return ("Player number: "+str(self.number)+", name: "+self.name+", units: "
                +str(self.units)+", terr: "+str(self.terr)+", cards: "+str(self.cards))    


#create initial data structures and randomize starting positions
#when called, name it 'Data' as this name is referenced in other class methods
class DataStructure():

    def __init__(self):
        self.players = 0
        self.terrList = []
        self.playerList = []
        self.turn = 0
        self.cardCount = 0
        self.cardAr = [4,6,8,10,12,15]
        self.neutral = False
        self.reset = False
        self.territoryData()

    #increase turn for next player
    def turnCounter(self):
        self.turn = (self.turn+1)%self.players

    def addNum(self):
        troops = self.playerList[self.turn].terr//3
        if troops < 3:
            troops = 3
        #add continent bonuses 
        for i in extra:
            contAr = extra[i]['terr']
            bonus = True
            for t in contAr:
                if self.terrList[t].owner != self.turn:
                    bonus = False
                    break
            if bonus:
                troops += extra[i]['units']
        return troops

    def getCardCash(self):
        playerCards = self.playerList[self.turn].cards
        if playerCards < 3:
            logging.warning('Not enough cards to cash')
            return 0
        else:
            self.playerList[self.turn].cards -= 3
            if self.cardCount <= 5:
                return self.cardAr[self.cardCount]
            else:
                return self.cardCount*5-10

    #check win state
    def checkWin(self):
        win = True
        for i in range(1,43):
            if self.terrList[i].owner != self.turn:
                if self.neutral and self.terrList[i].owner == 2:
                    continue
                else:
                    win = False
                    break
        return win

    #set up array of territory objects
    def territoryData(self):
        #zeroth-index is water
        water = Territory(None)
        water.RGB = water
        self.terrList.append(water)
        for i in range(1,43):
            t = Territory(i)
            self.terrList.append(t)

    #set up array of players 
    def playerData(self):
        for i in range(self.players):
            p = Player(i)
            self.playerList.append(p)
        #handle for neutral player if 2 players
        if self.players == 2: 
            n = Player(2)
            n.name = "Neutral"
            n.color = lightGrey
            n.bright = lightGrey #same color since it will never be highlighted
            self.neutral = True
            self.playerList.append(n)

    #random ownership/units depending on number of players
    #NOTE: terrData and playerList must be called first and passed in
    def randomStart(self):
        troopNum = {2:40, 3:35, 4:30, 5:25, 6:20}
        troops = [troopNum[self.players]]*(self.players+self.neutral)
        #randomly pick first player when setting countries
        first = random.randint(0,self.players+self.neutral)
        #set inital territories owners
        for i in range(42):
            p = (i+first)%(self.players+self.neutral)
            while True:
                r = random.randint(1,42)
                if self.terrList[r].owner == None:
                    self.terrList[r].owner = p
                    self.terrList[r].units = 1
                    self.playerList[p].units += 1
                    self.playerList[p].terr += 1
                    troops[p] -= 1
                    break
        #add remaining troops to territories
        for j in range(len(troops)):
            while troops[j] > 0:
                r = random.randint(1,42)
                if self.terrList[r].owner == j:
                    self.terrList[r].units += 1
                    self.playerList[j].units += 1
                    troops[j] -= 1

    #call all class methods to create inital startup
    def begin(self, players):
        if 2 > players > 6:
            logging.error('Invalid number of players')
        self.players = players
        self.playerData()
        self.randomStart()
        #randonly decide who goes first
        self.turn = random.randint(1,self.players-1)
    
    def restart(self, players):
        self.players = players
        self.terrList = []
        self.playerList = []
        self.turn = random.randint(1,self.players-1)
        self.cardCount = 0
        self.neutral = False
        self.reset = False
        self.territoryData()
        self.playerData()
        self.randomStart()
        
#iniitialize Data - this must be done here as RiskGUI.py and RiskMoves.py both
#utilize information from RiskData.py
Data = DataStructure()
