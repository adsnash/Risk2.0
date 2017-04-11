#! python3

from RiskData import Data
from RiskGUI import GUI
from RiskGUI import UI
from RiskIntro import Intro
import RiskMoves

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
