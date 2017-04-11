#! python3

import pygame
from pygame.locals import *
import logging
import random
import sys
import time
from RiskData import Data
from RiskGUI import GUI
from RiskGUI import UI
from RiskIntro import Intro


#handle mouse click/position, highlight menu, next, and numbers when available
def getMouseClick(hover=False):
    pygame.event.pump()
    pygame.event.clear()
    while True:
        (x,y) = pygame.mouse.get_pos()
        #highlight playerToken when mouse hovers over it
        if 304 < x < 333 and 518 < y < 547:
            if UI.tokenHover == False:
                UI.tokenHover = True
                UI.playerToken()
        #highlight nextButton when mouse hovers over it
        elif hover and 617 < x < 717 and 518 < y < 547:
            if UI.nextHover == False:
                UI.nextHover = True
                UI.nextButton()
        #highlight numberBoxes when mouse hovers over it
        elif hover == None:
            click = pygame.mouse.get_pressed()
            margin = 80
            for i in range(3):
                if (405+margin*i) < x < (405+margin*i+30) and (470) < y < (470+30):
                    if UI.numBoxAr[i] == Data.playerList[Data.turn].color:
                        color = Data.playerList[Data.turn].bright
                        UI.makeButton(color,(405+margin*i),470,30,30,str(i+1),20)
                else:
                    color = UI.numBoxAr[i]
                    UI.makeButton(color,(405+margin*i),470,30,30,str(i+1),20)
        else:
            if UI.tokenHover == True:
                UI.tokenHover = False
                UI.playerToken()
            elif UI.nextHover == True:
                UI.nextHover = False
                UI.nextButton()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #handle for left and right click. 1 for left click, 3 for right
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: 
                    return (event.pos, event.button)
                elif event.button == 3:
                    return (event.pos, event.button)                

class MoveSet():

    def __init__(self):
        self.player = 0
        self.addCard = False
        self.pick = True
        self.choice = False
        self.done = True
        self.troops = 0
        self.numAttackers = 0
        self.restart = False

    #reset flags for start of move
    def startMove(self):
        self.player = Data.turn
        self.addCard = False
        self.pick = True
        self.choice = False
        self.done = True
        self.troops = 0

    #set flags to pass through rest of move if rematch selected from menu
    def breakMove(self):
        self.pick = False
        self.choice = False
        self.done = False
        self.restart = True
        self.troops = 0

    #get clicks for any player owned territory
    #style: True for attack, False for fortify, None for placing units
    def clickMapAny(self, style=None):
        button = False
        if style != None:
            button = True
        while True and not self.restart:
            (x,y), click = getMouseClick(button)
            if y > 512:
                #handle for button and menu
                if 305 < x < 333 and 518 < y < 546:
                    Intro.menu()
                    if Data.reset == True:
                        logging.info('Restart selected')
                        self.breakMove()
                        if style == None:
                            return None, None
                        else:
                            return None
                if button and 618 < x < 717 and 518 < y < 546:
                    return False
                else:
                    continue
            else:
                p = GUI.MasterMap.get_at((x,y))
                #output not owned territory
                if 0 < p[0] < 43 and Data.terrList[p[0]].owner != self.player:
                    logging.info('Not your territory')
                    UI.box3 = 'Must select your own territory'
                    UI.update()
                    time.sleep(.05)
                    continue
                elif 0 < p[0] < 43 and Data.terrList[p[0]].owner == self.player:
                    #None for placing units
                    if style == None:
                        return p[0], click
                    #handle for right click
                    elif click == 3:
                        continue
                    #handle for too few units
                    elif click == 1 and Data.terrList[p[0]].units < 2:
                        GUI.highlight(p[0], True)
                        logging.info('Must have more than 1 unit')
                        UI.box3 = 'Must have more than 1 unit'
                        UI.update()
                        time.sleep(.05)
                        GUI.highlight(p[0], False)
                        continue
                    #attack/fortify
                    elif click == 1 and Data.terrList[p[0]].units > 1:
                        #make sure there are targets to pick from
                        targets = False
                        for i in Data.terrList[p[0]].touch:
                            #True for attack, False for fortify
                            if style and Data.terrList[i].owner != self.player:
                                UI.box2 = ('Select enemy territory to attack')
                                UI.box3 = ('Click water/same territory to reset')
                                UI.update()
                                targets = True
                                break
                            elif not style and Data.terrList[i].owner == self.player:
                                targets = True
                                UI.box3 = 'Territories must be touching'
                                break
                        #needs output to user
                        if targets:
                            GUI.highlight(p[0], True)
                            return p[0]
                        #handle for no enemies to attack
                        else:
                            GUI.highlight(p[0], True)
                            logging.info('No valid connecting territories')
                            UI.box3 = 'No valid connecting territories'
                            UI.update()
                            time.sleep(.05)
                            GUI.highlight(p[0], False)
                            continue

    #get clicks when specific countries must be clicked
    #style: number for redistribute, False for fortify, None for attack
    def clickMapSpecific(self, base, style=None):
        while True and not self.restart:
            GUI.drawLines(base, style)
            #add numberBox here - or in clickMapSpecific
            if style == None:
                UI.numBoxSetArray(base, self.numAttackers)
                UI.numBox()
                #could be handled with a none
                (x,y), click = getMouseClick(style)
            else:
                (x,y), click = getMouseClick()
            if y > 512:
                #handle for menu - button will not be live
                if 305 < x < 333 and 518 < y < 546:
                    Intro.menu()
                    if Data.reset == True:
                        logging.info('Restart selected')
                        self.breakMove()
                        if style == None:
                            return None
                        else:
                            return None, None 
                else:
                    continue
            else:
                waterBreak = True
                #set self.numAttackers without resetting from water click
                margin = 80
                for i in range(3):
                    if style == None and (405+margin*i) < x < (405+margin*i+30) and (470) < y < (470+30):
                        self.numAttackers = i+1
                        waterBreak = False
                p = GUI.MasterMap.get_at((x,y))
                #handle for water click reset
                if p[0] == 162 and style == None and waterBreak:
                    self.choice = False
                    logging.info('Water clicked - resetting')
                    UI.box2 = ('Resetting selected territory')
                    UI.box3 = ('Select territory to attack from')
                    UI.update()
                    GUI.highlight(base, False)
##                    GUI.setMap() #redundant
                    return False
                elif 0 < p[0] < 43:
                    #redistribute - only base or conquered territory
                    if type(style) is int and 0 < style < 43:
                        if p[0] == style or p[0] == base:
                            return p[0], click
                        else:
                            logging.info('Must be attacking or new territory')
                            UI.box3 = 'Must be attacking or new territory'
                            UI.update()
                            continue
                    else:
                        if p[0] not in Data.terrList[base].touch or p[0] != base:
                            logging.info('Territories must be touching')
                            UI.box2 = 'Territories must be touching'
                        if p[0] in Data.terrList[base].touch or p[0] == base:
                            #fortify - base or connected owned territories
                            if style == False:
                                if Data.terrList[p[0]].owner == self.player:
                                    return p[0], click
                                else:
                                    logging.info('Must choose your own territory')
                                    UI.box3 = 'Must choose your own territory'
                                    UI.update()
                                    continue
                            #attack - connected non-owned territories
                            elif style == None:
                                if Data.terrList[p[0]].owner != self.player:
                                    return p[0]
                                #handle for clicking same country - reset
                                elif p[0] == base:
                                    self.choice = False
                                    logging.info('Resetting selected territory')
                                    UI.box2 = ('Resetting selected territory')
                                    UI.box3 = ('Select territory to attack from')
                                    UI.update()
                                    GUI.highlight(p[0], False)
                                    return False
                                else:
                                    logging.info('Cannot attack owned territory')
                                    UI.box2 = 'Cannot attack owned territory'
                                    UI.update()
                                    continue

    #place troops on the map - left click for 1, right click for 5 or max
    #base = None; style = None: for any owned territory - normal placement
    #base = number; style: False for fortify, number for redistribute
    def placement(self, troops, base=None, style=None):
        troops = troops
        def placing(num):
            Data.terrList[terr].units += num
            if base == None:
                Data.playerList[self.player].units += num
##            GUI.displayUnits() #redundant?
            if num > 1:
                UI.box3 = str(num)+' troops added'
            else:
                UI.box3 = str(num)+' troop added'
            UI.update()
            GUI.highlight(terr, True)
        UI.nextColor = False
        #loop while there are troops to place
        while troops > 0 and not self.restart:
            UI.box2 = str(troops)+' unit(s) to place'
            UI.update()
            if style == None:
                terr, click = self.clickMapAny()
            else:
                GUI.drawLines(base, style)
                terr, click = self.clickMapSpecific(base, style)
            if click != None:
                #left click places one unit
                if click == 1:
                    placing(1)
                    troops -= 1
                #right click places multiple units - 10, 5, or remaining
                elif click == 3:
                    #if more than 50 troops to place, place 10 at a time
                    if troops >= 50:
                        placing(10)
                        troops -= 10
                    #if less than 50 but more than 5, place 5 at a time
                    elif 50 > troops > 5:
                        placing(5)
                        troops -= 5
                    #if less than 5 troops, place remaining 
                    else:
                        placing(troops)
                        troops -= troops
                time.sleep(.05)
                GUI.highlight(terr, False)

    #choice to cash cards - True for begin turn, False after eliminating player
    def cardChoice(self, style):
        bonus = 0
        cashing = style
        additional = False
        #handle for eliminated player
        if not style:
            cards = Data.playerList[self.player].cards
            if cards >= 6:
                while cards > 4:
                    bonus += Data.getCardCash()
                    Data.cardCount += 1
                    cards -= 3
                if bonus > 0:
                    UI.box3 = ('Cards cashed - '+str(bonus)+' extra units')
                    UI.update()
            return bonus
        #handle for beginning of turn
        while cashing and not self.restart:
            cards = Data.playerList[self.player].cards
            if cards < 3:
                #not enough to cash
                cashing = False
                if bonus == 0:
                    UI.box3 = 'Select territories to place units'
                return bonus
            elif cards >= 5:
                #forced to cash
                bonus += Data.getCardCash()
                Data.cardCount += 1
                logging.info('Cards cashed - '+str(bonus)+' extra units')
                UI.box3 = ('Cards cashed - '+str(bonus)+' extra units added')
                UI.update()
                additional = True
            elif 3 <= cards < 5:
                #handle if given a choice to cash
                if additional:
                    UI.box1 = Data.playerList[self.player].name+' - '+str(self.troops+bonus)+' to Place'
                    UI.box2 = 'Would you like to cash extra cards?'
                else:
                    UI.box2 = 'Would you like to cash your cards?'
                    UI.box3 = 'Click \'Cash\' if so or click the map'
                UI.nextMsg = 'Cash'
                UI.nextColor = True
                UI.nextHover = False
                UI.update()
                #get click - map if not cashing, button if cashing
                while True and not self.restart:
                    (x,y), click = getMouseClick(True)
                    if y < 512:
                        logging.info('Player not cashing')
                        cashing = False
                        return bonus
                    elif 305 < x < 333 and 518 < y < 546:
                        Intro.menu()
                        if Data.reset == True:
                            logging.info('Restart selected')
                            self.breakMove()
                            return None
                    elif 618 < x < 717 and 518 < y < 546:
                        if click == 1:
                            bonus += Data.getCardCash()
                            Data.cardCount += 1
                            logging.info('Cards cashed - '+str(bonus)+' extra units')
                            UI.box3 = ('Cards cashed - '+str(bonus)+' extra units added')
                            choice = False
                            return bonus
                    else:
                        continue

    #roll dice for attack - use max for defender, currently max for attacker
    def dice(self, attacker, defender):
        attTotal = Data.terrList[attacker].units
        #make sure too many units aren't selected for attacking
        if self.numAttackers > attTotal - 1:
            logging.error('Too many attackers selected')
        defTotal = Data.terrList[defender].units
        defPlayer = Data.terrList[defender].owner
        defNum = min(2, defTotal)
        attAr,defAr = [],[]
        attLoss,defLoss = 0,0
        change = None
        for i in range(self.numAttackers):
            n = random.randint(1,6)
            attAr.append(n)
        for j in range(defNum):
            n = random.randint(1,6)
            defAr.append(n)
        attAr.sort(reverse=True)
        defAr.sort(reverse=True)
        for i in range(min(self.numAttackers, defNum)):
            if attAr[i] > defAr[i]:
                defLoss += 1
                Data.playerList[defPlayer].units -= 1
                Data.terrList[defender].units -= 1
            else:
                attLoss += 1
                Data.playerList[self.player].units -= 1
                Data.terrList[attacker].units -= 1
        if Data.terrList[defender].units < 1:
            Data.playerList[self.player].terr += 1
            Data.playerList[defPlayer].terr -= 1
            Data.terrList[defender].owner = self.player
            Data.terrList[defender].units += self.numAttackers
            Data.terrList[attacker].units -= self.numAttackers
            change = True
        elif Data.terrList[attacker].units < 2:
            change = False
        return attLoss, defLoss, change

    #returns True for elimination (and takes cards), False if not
    def eliminated(self, defender):
        if Data.playerList[defender].units == 0 and Data.playerList[defender].terr == 0:
            c = Data.playerList[defender].cards
            Data.playerList[defender].cards = 0
            Data.playerList[self.player].cards += c
            UI.eliminatedLine(defender)
            UI.update()
            return True
        return False
        
    #get starting number of troops + card bonuses and place on territories
##    def startingPlace(self):
##        UI.box1 = Data.playerList[self.player].name+' - Add Units'
##        bonus = self.cardChoice(True)
##        if bonus != None:
##            troops = Data.addNum()
##            number = bonus + troops
##            UI.nextMsg = 'Attack'
##            UI.update()
##            logging.info(str(number)+' troops to add')
##            self.placement(number)
    def startingPlace(self):
        self.troops = Data.addNum()
        UI.box1 = Data.playerList[self.player].name+' - '+str(self.troops)+' to Place'
        bonus = self.cardChoice(True)
        if bonus != None:
            self.troops += bonus
            UI.nextMsg = 'Attack'
            UI.box1 = Data.playerList[self.player].name+' - Place Units'
            UI.box3 = 'Click territories to place units'
            UI.update()
            logging.info(str(self.troops)+' troops to add')
            self.placement(self.troops)

    #handle for color change, check for win, elimination, and redistribute
    def territoryConquered(self, base, target, defender):
        self.addCard = True
        self.choice = False
        GUI.updateBoard(target)
        GUI.highlight(base, False) 
        self.eliminated(defender)
        if Data.checkWin():
            #break out of attack - handle win
            logging.info(Data.playerList[self.player].name+' wins')
            UI.box1 = Data.playerList[self.player].name+' Wins!'
            UI.box2 = 'World Domination Complete'
            UI.box3 = 'Interested in a rematch?'
            UI.update()
            self.pick = False
        else:
            logging.info('Territory conquered')
            UI.box3 = 'Territory conquered'
            UI.update()
            if Data.terrList[base].units > 1:
                troops = Data.terrList[base].units - 1
                Data.terrList[base].units -= troops
                GUI.displayUnits() #take out if not correct
                GUI.drawLines(base, target)
                self.placement(troops, base, target)
                #GUI.setMap()
            bonus = self.cardChoice(False)
            if bonus > 0:
                self.placement(bonus)

    #select attacking territory, number of units (default is always max, but
    #other amounts allowed), and connected target territory
    def attack(self):
        UI.nextMsg = 'Fortify'
        UI.nextHover = False
        UI.update()
        #loop to get appropriate attacking territory or advance to fortify
        while self.pick and not self.restart:
            UI.nextColor = True
            UI.box1 = Data.playerList[self.player].name+' - Attack'
            UI.box2 = 'Select one of your territories'
            UI.box3 = 'to launch attack from'
            UI.update()
            base = self.clickMapAny(True)
            if base == None or not base:
                self.pick = False
            else:
                self.choice = True
                #set default troops to max attackers, can be changed by player
                self.numAttackers = min(Data.terrList[base].units-1, 3)
                UI.numBoxSetArray(base, self.numAttackers)
                #loop to get target or handle break to send back to first loop
                while self.choice and not self.restart:
                    UI.nextColor = False
                    UI.update()
                    GUI.drawLines(base, None)
                    UI.numBox() #redundant call?
                    target = self.clickMapSpecific(base)
                    if target != None and target != False:
                        #roll dice, handle results
                        defender = Data.terrList[target].owner
                        attLoss, defLoss, change = self.dice(base, target)
                        logging.info('Attacker lost '+str(attLoss)+', defender lost '+str(defLoss)+', change: '+str(change))
                        UI.box2 = ('You lost '+str(attLoss)+', defender lost '+str(defLoss))
                        UI.box3 = ('Click to attack again or water to reset')
                        UI.update()
                        #handle for less available attackers
                        if Data.terrList[base].units-1 < self.numAttackers:
                            self.numAttackers = Data.terrList[base].units-1
                        GUI.displayUnits()
                        #not enough units to keep attacking
                        if change == False:
                            logging.info('Too few units to continue attacking')
                            GUI.highlight(base, False)
                            GUI.highlight(target, False)
                            self.choice = False
                        #territory conquered
                        if change:
                            self.territoryConquered(base, target, defender)

    #move units between owned connected territories, only when attack finishes
    def fortify(self):
        UI.nextMsg = 'End Turn'
        UI.nextHover = False
        UI.box1 = Data.playerList[self.player].name+' - Fortify'
        UI.update()
        while self.done and not self.restart:
            UI.nextColor = True
            UI.box2 = ('Select territory to move units')
            UI.box3 = ('Click \'End Turn\' when finished')
            UI.update()
            base = self.clickMapAny(False)
            if base == None or not base:
                break 
            else:
##                GUI.highlight(base, False)
                troops = Data.terrList[base].units - 1
                Data.terrList[base].units -= troops
##                GUI.displayUnits()
                GUI.highlight(base, False)
                self.placement(troops, base, False)
                GUI.setMap() #redundant?

    #handle for rematch after victory 
    def rematch(self):
        UI.nextMsg = 'Rematch'
        UI.nextColor = True
        UI.nextHover = True
        UI.update()
        while True and not self.restart:
            (x,y), click = getMouseClick(True)
            if 305 < x < 333 and 518 < y < 546:
                Intro.menu()
                if Data.reset == True:
                    self.breakMove()
            elif 618 < x < 717 and 518 < y < 546:
                if click == 1:
                    #handle for rematch
                    logging.info('Rematch selected')
                    Data.reset = True
                    self.breakMove()
                    break #this can probably be removed
            else:
                continue

    #call all move methods in order - easier function call
    def fullMove(self):
        self.startMove()
        self.startingPlace()
        self.attack()
        if self.addCard:
            Data.playerList[self.player].cards += 1
        if Data.checkWin():
            self.rematch()
        else:    
            self.fortify()

#initialize Moves object - do in main?
#Moves = MoveSet()
