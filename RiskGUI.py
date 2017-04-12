#! python3

import pygame
from pygame.locals import *
import logging
import random
import sys
import time
from RiskData import Data
from RiskRaw import *

class GUI():
    
    def __init__(self, width=1000, height=612):
        self.width = width
        self.height = height
        #initialize pygame and display
        pygame.init()
        self.gameDisplay = pygame.display.set_mode((width,height), 0, 8)
        #set color palettes board and menu/intro 
        self.palette = self.startPalette()
        self.rainbowPalette = self.rainbowSet()
        pygame.display.set_caption('Risk Simulation by Alex Nash')
        #set icon image
        self.icon = pygame.image.load('RedR.png')
        pygame.display.set_icon(self.icon)
        #load in the map
        self.Map = pygame.image.load('Map.gif')
        self.Map.set_palette(self.palette)
        #second unseen map to track territory selection
        self.MasterMap = pygame.image.load('Map.gif')

    #set initial map palette to quickly change colors
    def startPalette(self):
        palette = []
        palette.append(water)
        for i in range(1,43):
            color = (i,150,100)
            palette.append(color)
        palette.append(black)
        return palette

    #create rainbow palette for intro/menu map
    def rainbowSet(self):
        def colorPicker(num):
            if num <= 9:
                return red
            elif 10 <= num <= 13:
                return orange
            elif 14 <= num <= 20:
                return yellow
            elif 21 <= num <= 26:
                return green
            elif 27 <= num <= 38:
                return blue
            elif 39 <= num <=42:
                return purple
        rainbowPalette = self.startPalette()
        for i in range(1,43):
            color = colorPicker(i)
            rainbowPalette[i] = color
        return rainbowPalette

    #switches to rainbow map and draws connecting lines for all territories
    def setMenu(self):
        self.Map.set_palette(self.rainbowPalette)
        self.gameDisplay.blit(self.Map, (0,0))
        UI.legend()
        for i in range(1,43):
            for j in Data.terrList[i].touch:
                self.drawLines(i,j)
    
    #functions for making boxes and text
    def makeText(self, msg, s=30):
        font = pygame.font.Font('freesansbold.ttf', s)
        text = font.render(msg, False, black)
        return text

    #re-blit map to wipe numbers/lines, place units on respective territories
    def displayUnits(self):
        self.gameDisplay.blit(self.Map, (0,0))
        UI.legend()
        for i in range(1,43):
            units = Data.terrList[i].units
            text = self.makeText(str(units), 20)
            coordinates = Data.terrList[i].coord
            self.gameDisplay.blit(text, coordinates)
        pygame.display.update()

    #draw lines connecting territories for options to click
    #other = number for one option, False for fortify, None for attack
    def drawLines(self, place, other):
        def getCoord(terr):
            C = Data.terrList[terr].coord
            ptC = (C[0]+5, C[1]+7)
            return ptC
        def getAlt(terr):
            ptC = Data.terrList[terr].alt
            return ptC
        #handle for Alaska/Eastern Russia so lines go to both ends of display
        def edgeCase():
            ptNA = getCoord(1)
            altNA = (2, ptNA[1])
            ptAS = getCoord(32)
            altAS = (997, ptAS[1])
            pygame.draw.line(self.gameDisplay, white, ptNA, altNA, 1)
            pygame.draw.line(self.gameDisplay, white, ptAS, altAS, 1)
        def pickCoord(terr):
            if Data.terrList[terr].alt != None:
                pt = getAlt(terr)
            else:
                pt = getCoord(terr)
            return pt
        def makeLines(first, second):
            if (first == 1 and second == 32) or (first == 32 and second == 1):
                edgeCase()
            else:
                pt1 = pickCoord(first)
                pt2 = pickCoord(second)
                pygame.draw.line(self.gameDisplay, white, pt1, pt2, 1)
        #post-attack fortify: only lines between attacking/conquered territory
        if type(other) is int and 0 < other < 43:
            makeLines(place, other)
        else:
            for i in Data.terrList[place].touch:
                #attack: lines to all non-player owned connected territories
                if other == None and Data.terrList[i].owner != Data.turn:
                    makeLines(place, i)
                #fortify: lines to all player owned connected territories
                elif other == False and Data.terrList[i].owner == Data.turn:
                    makeLines(place, i)
        pygame.display.update()

    #set map palette and place units
    def setMap(self):
        self.Map.set_palette(self.palette)
        self.displayUnits()
        UI.update()

    #highlight selected country, pass true/false for on/off
    def highlight(self, terr, style):
        owner = Data.terrList[terr].owner
        if style:
            color = Data.playerList[owner].bright
        elif not style:
            color = Data.playerList[owner].color
        if self.palette[terr] != color: 
            self.palette[terr] = color
            self.setMap()        

    #set current palette/static info - used at beginning to set up board
    def currentBoard(self):
        for i in range(1,43):
            owner = Data.terrList[i].owner
            self.palette[i] = Data.playerList[owner].color
        UI.staticInfo()
        self.setMap()

    #pass conquered territory, switch color - does not blit, highlight handles
    def updateBoard(self, conquered):
        owner = Data.terrList[conquered].owner
        self.palette[conquered] = Data.playerList[owner].color

#put msg boxes into 1 method, fix magic numbers or describe in comments
class UI():
    
    def __init__(self):
        self.width = GUI.width
        self.height = GUI.height
        self.box1 = 'Welcome to Risk!'
        self.box2 = 'Game loading...'
        self.box3 = 'Have fun!'
        self.nextMsg = 'Attack'
        self.nextColor = False
        self.nextHover = False
        self.tokenHover = False
        self.numBoxAr = []
        
    #functions for making boxes and text
    def makeText(self, msg, s=30):
        font = pygame.font.Font('freesansbold.ttf', s)
        text = font.render(msg, False, black)
        return text

    #if passed empty string, can be used to make a colored rectangle
    def makeButton(self, color, x, y, w, h, msg, s):
        pygame.draw.rect(GUI.gameDisplay, color, (x,y,w,h))
        text = self.makeText(msg, s)
        spot = text.get_rect()
        spot.center = ((x+w/2),(y+h/2+1))
        GUI.gameDisplay.blit(text, spot)
        pygame.display.update()

    #add number descriptors and player names/colors
    #call when resetting to handle for different number of players
    def staticInfo(self):
        self.makeButton(black,0,509,self.width,120,'',0)
        self.makeButton(grey,2,512,self.width-4,98,'',0)
        self.makeButton(black,278,514,444,94,'',0)
        players = Data.players
        xInc = 720
        yInc = 27
        s = (' '*3)
        self.makeButton(grey,110,515,160,15,('Units'+s+'Territories'+s+'Cards'),14)
        self.makeButton(grey,110+xInc,515,160,15,('Units'+s+'Territories'+s+'Cards'),14)
        for i in range(1,players+1):
            side = i%2
            down = (i+side)//2
            color = Data.playerList[i-1].color
            self.makeButton(grey,(750-xInc*side),(505+yInc*down),80,20,('Player '+str(i)),17)
            self.makeButton(black,(730-xInc*side),(506+yInc*down),18,18,'',0)
            self.makeButton(color,(732-xInc*side),(508+yInc*down),14,14,'',0)
        if players == 2:
            color = lightGrey
            self.makeButton(grey,(30),(559),80,20,('Neutral'),17)
            self.makeButton(black,(10),(560),18,18,'',0)
            self.makeButton(color,(12),(562),14,14,'',0)
        
    #display player info (units, territories, cards) - called when one changes
    def dynamicInfo(self):
        players = Data.players
        xInc = 720
        yInc = 27
        for i in range(1,players+1):
            side = i%2
            down = (i+side)//2
            u = str(Data.playerList[i-1].units)
            t = str(Data.playerList[i-1].terr)
            c = str(Data.playerList[i-1].cards)
            s = (' '*9)
            self.makeButton(grey,(830-xInc*side),(505+yInc*down),160,18,(u+s+t+s+c),17)
        if players == 2:
            u = str(Data.playerList[2].units)
            t = str(Data.playerList[2].terr)
            c = str(Data.playerList[2].cards)
            s = (' '*9)
            self.makeButton(grey,(830-xInc),(505+yInc*2),160,20,(u+s+t+s+c),17)

    #calls both static and dynamic info
    def info(self):
        self.staticInfo()
        self.dynamicInfo()

    #add static legend info and country bonuses to map
    def legendStatic(self):
        self.makeButton(black,18,330,142,160,'',0)
        self.makeButton(grey,20,332,138,156,'',0)
        self.makeButton(black,18,352,142,2,'',0)
        self.makeButton(black,18,466,142,2,'',0)
        self.makeButton(grey,22,332,136,20,'Legend',18)
        conts = ['North America','South America','Europe','Africa','Asia','Oceania']
        nums = ['5','2','5','3','7','2']
        for i in range(len(conts)):
            self.makeButton(grey,22,(356+19*i),120,15,conts[i],15)
            self.makeButton(grey,137,(356+19*i),20,15,nums[i],15)
        self.makeButton(grey,22,470,120,15,'Card Cash:',17)

    #add next card cash amount - updates when cards are cashed
    def legendDynamic(self):
        if Data.cardCount <= 5:
            c = Data.cardAr[Data.cardCount]
        else:
            c = (Data.cardCount)*5-10  
        self.makeButton(grey,135,472,20,15,str(c),15)

    #calls both static and dynamic legend
    def legend(self):
        self.legendStatic()
        self.legendDynamic()

    #generic message box function to output info to user
    def box(self, msg,y,w=440):
        x,h,s = 280, 30, 24
        self.makeButton(white,x,y,w,h,msg,s)

    #first message box - moves output left to compensate for button
    def msgBox1(self):
        y = 516
        w = 390
        msg = self.box1
        self.box(msg,y,w)
        self.makeButton(white,670,y,50,30,'',0)

    #second message box
    def msgBox2(self):
        y = 516+30
        msg = self.box2
        self.box(msg,y)

    #third message box
    def msgBox3(self):
        y = 516+60
        msg = self.box3
        self.box(msg,y)

    #player token - updates for player turn, highlights on hover, click for menu
    def playerToken(self):
        if self.tokenHover == True:
            color = Data.playerList[Data.turn].bright
        if self.tokenHover == False:
            color = Data.playerList[Data.turn].color
        self.makeButton(black,305,519,28,28,'',0)
        self.makeButton(color,309,523,20,20,'',0)

    #used with getMouseClick to make grey or red, will highlight if hovered 
    def nextButton(self):
        if self.nextColor == True and self.nextHover == False:
            color = red
        elif self.nextColor == True and self.nextHover == True:
            color = brightRed
        else:
            color = grey
        self.makeButton(black,617,519,100,28,'',0)
        self.makeButton(color,621,523,92,20,self.nextMsg,20)

    #set number box array for selecting # units to attack with - defaults to max
    def numBoxSetArray(self, terr, curr):
        self.numBoxAr = []
        number = min(Data.terrList[terr].units-1, 3)
        for i in range(3):
            if int(i+1) > int(number):
                color = grey
            elif int(i+1) == int(curr):
                color = Data.playerList[Data.turn].bright
            else:
                color = Data.playerList[Data.turn].color
            self.numBoxAr.append(color)
                

    #draw number boxes for selecting # units to attack with
    def numBox(self):
        msg = "How many units would you like to attack with?"
        self.makeButton(water,450,438,100,20,msg,17)
        margin = 80
        for i in range(3):
            self.makeButton(black,(400+margin*i),465,40,40,'',0)
            color = self.numBoxAr[i]
            self.makeButton(color,(405+margin*i),470,30,30,str(i+1),20)

    #draw line through eliminated player, color of player who did eliminating
    def eliminatedLine(self, defender):
        spot = defender+1
        xInc = 720
        yInc = 27
        side = spot%2
        down = (spot+side)//2
        color = Data.playerList[Data.turn].color
        self.makeButton(black,(725-xInc*side),(513+yInc*down),105,4,'',0)
        self.makeButton(color,(726-xInc*side),(514+yInc*down),103,2,'',0)
        UI.update()

    #wrap up functions to update changing of user interface with one method
    def update(self):
        self.msgBox1()
        self.msgBox2()
        self.msgBox3()
        self.nextButton()
        self.playerToken()
        self.dynamicInfo()
        self.legendDynamic()
        

#iniitialize user interface
GUI = GUI()
UI = UI()

