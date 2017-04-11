#! python3

import pygame
import logging
import sys
from RiskData import Data
from RiskGUI import GUI
from RiskGUI import UI
from RiskRaw import *

#used for intro and menu screens, initialized at bottom of file
#call 'Intro' to work with RiskMoves.py references
class Introduction():

    #menu for when player token is clicked
    #handles for tutorial, hints, restart, and resume game
    def menu(self):
        UI.info()
        GUI.setMenu()
        UI.makeButton(white,280,516,440,90,'',0)
        UI.makeButton(black,480,529,40,40,'',0)
        UI.makeButton(Data.playerList[Data.turn].color,485,534,30,30,'',0)
        UI.makeButton(white,440,578,120,20,Data.playerList[Data.turn].name,20)
        col = [red,yellow,green,blue]
        bri = [brightRed,brightYellow,brightGreen,brightBlue]
        msg = ['Resume','Restart','Tutorial','Hints']
        xInc = 255
        yInc = 49
        menu = True
        style = None
        for i in range(4):
            side = i%2
            down = i//2
            UI.makeButton(black,(305+side*xInc),(519+down*yInc),135,35,'',0)
            UI.makeButton(col[i],(310+side*xInc),(524+down*yInc),125,25,msg[i],25)
        while menu:
            pygame.event.pump()
            pygame.event.clear()
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            #highlight/get click if mouse enters player token
            if (480) < mouse[0] < (480+40) and (529) < mouse[1] < (529+40):
                UI.makeButton(Data.playerList[Data.turn].bright,485,534,30,30,'',0) 
                if click[0] == 1:
                    style = 0
                    menu = False
            else:
                UI.makeButton(Data.playerList[Data.turn].color,485,534,30,30,'',0)
            for j in range(4):
                side = j%2
                down = j//2
                #highlight/get click if mouse enters button
                if (305+side*xInc) < mouse[0] < (305+side*xInc+135) and (519+down*yInc) < mouse[1] < (519+down*yInc+35):
                    UI.makeButton(bri[j],(310+side*xInc),(524+down*yInc),125,25,msg[j],25)
                    if click[0] == 1:
                        style = j
                        menu = False
                else:
                    UI.makeButton(col[j],(310+side*xInc),(524+down*yInc),125,25,msg[j],25)
        #handle each button with appropriate method
        if style == 0:
            GUI.setMap()
        if style == 1:
            self.confirm()
        if style == 2:
            self.tutorial(True)
        if style == 3:
            self.hints()

    #confirm restart - adds yes/no buttons to screen, requires one be pressed
    def confirm(self):
        msg = "Are you sure? This action cannot be undone."
        UI.makeButton(water,450,440,100,20,msg,17)
        UI.makeButton(black,365,470,110,35,'',0)
        UI.makeButton(green,370,475,100,25,'Yes',20)
        UI.makeButton(black,525,470,110,35,'',0)
        UI.makeButton(red,530,475,100,25,'No',20)
        confirm = True
        choice = False
        while confirm:
            pygame.event.pump()
            pygame.event.clear()
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            #highlight yes button and handle click
            if (365) < mouse[0] < (365+110) and (470) < mouse[1] < (470+35):
                UI.makeButton(brightGreen,370,475,100,25,'Yes',20)
                if click[0] == 1:
                    logging.info('Player clicked to restart')
                    choice = True
                    confirm = False
            #highlight no button and handle click
            elif (530) < mouse[0] < (530+110) and (470) < mouse[1] < (470+35):
                UI.makeButton(brightRed,530,475,100,25,'No',20)
                if click[0] == 1:
                    confirm = False
            else:
                UI.makeButton(green,370,475,100,25,'Yes',20)
                UI.makeButton(red,530,475,100,25,'No',20)
        if choice:
            Data.reset = True
            return False
        else:
            self.menu()

    #accessible via menu, provides helpful hints for players
    def hints(self):
        UI.makeButton(black,0,0,GUI.width,GUI.height,'',0)
        UI.makeButton(grey,2,2,GUI.width-4,GUI.height-4,'',0)
        msgA = "Try to take the smaller continents like South America or Australia, especially early on."
        msgB = "If an opponent holds a continent, take one of its territories to prevent him getting the bonus."
        msgC = "Card cash is the key to victory – every subsequent amount will be larger than the last."
        msgD = "Eliminating opponents gives you their cards – try to string together multiple eliminations."
        msgE = "If you don’t have any good moves, if you can, try to take at least one territory to get cards for the round."
        msgF = "Attack with at least 3 attackers (meaning at least four units in the territory) for the best odds of success."
        msgG = "Consolidate your forces – if your attackers falls below 3, you reduce your odds of success."
        msgH = "When holding a continent, place troops at the borders rather than spreading throughout the continent."
        msgI = "Watch where your opponent fortifies his troops, it may tip you off to his next move."
        msgAr = [msgA,msgB, msgC, msgD, msgE, msgF, msgG, msgH, msgI]
        UI.makeButton(grey,250,40,500,50,'Here are some hints - hope they help!',45)
        down = 35
        for i in range(len(msgAr)):
            UI.makeButton(grey,150,(120+(down)*i),700,30,msgAr[i],18)
        UI.makeButton(black,385,480,180,60,'',0)
        UI.makeButton(red,390,485,170,50,'Got it!',30)
        hint = True
        while hint:
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if (390) < mouse[0] < (390+170) and (480) < mouse[1] < (480+60):
                UI.makeButton(brightRed,390,485,170,50,'Got it!',30)
                if click[0] == 1:
                    hint = False
            else:
                UI.makeButton(red,390,485,170,50,'Got it!',30)
            pygame.display.update()
        self.menu()

    #initial tutorial - pass True for menu version that returns back to menu
    def tutorial(self, style=False):
        UI.makeButton(black,0,0,GUI.width,GUI.height,'',0)
        UI.makeButton(grey,2,2,GUI.width-4,GUI.height-4,'',0)
        msgA = "This is a Risk simulation I built in python to practice programming. I hope you enjoy it!"
        msgB = "Please take note - there are a few changes from the original rules:"
        msgC = "Initial territory and troop placement is randomized."
        msgD = "Cards have been simplified. You may cash your cards when you have 3 or 4."
        msgE = "Cards are automatically cashed when you have 5 or more."
        msgF = "Attacking territories will default to use the maximum number of dice, but can be changed."
        msgG = "Defending territories will automatically use the maximum number of dice."
        msgH = "Pro Tip: when placing units, you can left click to add 1 or right click to add 5."
        msgI = "If there are less than 5 to add, all of the remaining units will be added."
        msgJ = "You can check out the source code on my github: https://github.com/adsnash"
        msgK = "If you are unfamiliar with the rules of Risk, please visit: http://www.hasbro.com/common/instruct/risk.pdf"
        msgL = "Legal disclaimer: Risk is a registered trademark of Parker Brothers. This simulation is for educational purposes only."
        msgM = "I do not claim to own any of Parker Brothers’ intellectual property. Please don’t sue me!"
        msgAr = [msgB,msgC,msgD,msgE,msgF,msgG,msgH,msgI]
        UI.makeButton(grey,250,20,500,50,'Welcome to my Risk Simulation!',45)
        UI.makeButton(grey,150,80,700,25,msgA,16)
        down = 30
        for i in range(len(msgAr)):
            UI.makeButton(grey,150,(120+(down)*i),700,30,msgAr[i],20)
        UI.makeButton(grey,50,460,900,20,msgJ,16)
        UI.makeButton(grey,50,490,900,20,msgK,16)
        UI.makeButton(grey,50,530,900,20,msgL,13)
        UI.makeButton(grey,50,555,900,20,msgM,13)
        UI.makeButton(black,385,380,180,60,'',0)
        UI.makeButton(red,390,385,170,50,'Got it!',30)
        intro = True
        while intro:
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if 390 < mouse[0] < 390+170 and 385 < mouse[1] < 435:
                UI.makeButton(brightRed,390,385,170,50,'Got it!',30)
                if click[0] == 1:
                    intro = False
            else:
                UI.makeButton(red,390,385,170,50,'Got it!',30)
        if style:
            self.menu()

    #initial map shown during intro, same map as menu
    def introMap(self):
        intro = True
        GUI.setMenu()
        msgA = "This map shows the different continents and the connections between territories."
        msgB = "Click the current player at token any time to see this map again."
        msgC = "Please note: the button to move to the next phase of your turn will be red when active or grey if action must be taken."
        msgAr = [msgA,msgB,msgC]
        UI.makeButton(black,0,512,GUI.width,100,'',0)
        UI.makeButton(grey,2,513,GUI.width-4,97,'',0)
        down = 30
        for i in range (3):
            UI.makeButton(grey,50,(520+down*i),900,20,msgAr[i],16)
        UI.makeButton(black,385,445,180,60,'',0)
        UI.makeButton(red,390,450,170,50,'Let\'s Play!',30)
        while intro:
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if 390 < mouse[0] < 390+170 and 450 < mouse[1] < 500:
                UI.makeButton(brightRed,390,450,170,50,'Let\'s Play!',30)
                if click[0] == 1:
                    intro = False
            else:
                UI.makeButton(red,390,450,170,50,'Let\'s Play!',30)

    #get number of players, reused for rematch to get new number
    def pickPlayer(self):
        UI.makeButton(black,0,0,GUI.width,GUI.height,'',0)
        UI.makeButton(grey,2,2,GUI.width-4,GUI.height-4,'',0)
        UI.makeButton(grey,250,100,500,100,'Get ready to start!',50)
        UI.makeButton(grey,250,200,500,100,'How many players?',40)
        margin = 130
        col = [red,blue,green,yellow,purple]
        bri = [brightRed,brightBlue,brightGreen,brightYellow,brightPurple]
        for i in range(5):
            c = col[i]
            UI.makeButton(black,(195+margin*i),345,90,90,'',0)
            UI.makeButton(c,(200+margin*i),350,80,80,str(i+2),38)
        picking = True
        numberPlayers = 0
        while picking:
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            #highlight number buttons
            for j in range(5):
                if (195+margin*j) < mouse[0] < (195+margin*j+90) and (345) < mouse[1] < (345+90):
                    c = bri[j]
                    UI.makeButton(c,(200+margin*j),350,80,80,str(j+2),38)
                    if click[0] == 1:
                        #get number of players
                        numberPlayers = j+2
                        picking = False
                else:
                    c = col[j]
                    UI.makeButton(c,(200+margin*j),350,80,80,str(j+2),38)
        logging.info(str(numberPlayers)+' players selected')
        return numberPlayers

    def fullIntro(self):
        self.tutorial()
        self.introMap()
        numberPlayers = self.pickPlayer()
        return numberPlayers

#initialize intro - utilized by RiskMoves.py
Intro = Introduction()
