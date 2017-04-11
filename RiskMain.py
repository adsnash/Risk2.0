#! python3

from RiskData import Data
from RiskGUI import GUI
from RiskGUI import UI
from RiskIntro import Intro
#initialize locally?
#from RiskMoves import Moves
import RiskMoves

#for testing purposes
def finish4():
    for i in range(1,40):
        Data.terrList[i].owner = 0
        Data.terrList[i].units = 1
    Data.terrList[40].owner = 1
    Data.terrList[40].units = 1
    Data.terrList[41].owner = 2
    Data.terrList[41].units = 1
    Data.terrList[42].owner = 3
    Data.terrList[42].units = 1
    Data.playerList[0].cards = 7
    Data.playerList[0].terr = 39
    Data.playerList[0].units = 39
    for j in range(1,4):
        Data.playerList[j].cards = 4
        Data.playerList[j].terr = 1
        Data.playerList[j].units = 1


#def realMain():
#uncomment for actual main function
def main():
    
    Moves = RiskMoves.MoveSet()
    while True:
        if Data.reset:
            num = Intro.pickPlayer()
            Data.restart(num)
            Moves.restart = False
        else:
            num = Intro.fullIntro()
            Data.begin(num)
        #take this out to actually play
        if Data.players == 4:
            finish4()

        GUI.currentBoard()
        gameLoop = True
        while not Moves.restart:
            #check that player is still in the game
            if Data.playerList[Data.turn].units > 0 and Data.playerList[Data.turn].units > 0:
                Moves.fullMove()
                Data.turnCounter()
            else:
                Data.turnCounter()


if __name__ == '__main__':
    main()
