"""
home.py
created by Rachel Kim (rhkim)
 for 15-112 F15 Term Project

 home page; instructions pages
 uses pygame events to get the user's mouse clicks for buttons
"""

import pygame, os
import random
from helper import *
class StartUp:
    def __init__(self):
        self.mousex = self.mousey = None

        self.startMode = 0 #0-start; 1-instructions1; 2-instructions2; 3-instructions3; 5-select level
        self.buttonPressed = None

        self.playButton = (222,231,385,293) #x1,y1,x2,y2
        
        self.instructButton = (126,310,282,384)
        self.instructPlayButton = (25,462,176,515)
        self.backButton =  (320,462,444,520)
        self.nextButton = (470,462,590,520)
        
        self.levelButton = (326,210,480,384)
        self.homeButton = (94, 445, 282, 503)
        self.randomButton = (325, 445, 512, 503)
        self.getLevelButtons()

        
        self.loadimages()
        self.frameCount = 0
        self.level = 0

    def loadimages(self):
        self.startPage1,null = load_image('start1.gif')
        self.startPage2,null = load_image('start2.gif')
        self.startPage3,null = load_image('start3.gif')
        self.startPage = [self.startPage1, self.startPage2, self.startPage3]
        self.instructions1,null = load_image('instructions1.gif')
        self.instructions2,null = load_image('instructions2.gif')
        self.instructions3,null = load_image('instructions3.gif')
        self.instructions = [self.instructions1, self.instructions2, self.instructions3]
        self.levelsPage,null = load_image('levels.gif')

    def getLevelButtons(self):
        x, y = (36, 146)
        width, height = 72, 58
        xspace, yspace = 44, 40
        level = 1
        self.levelButttons = dict()
        for col in range(3):
            ytop = y + (height + yspace) * col
            ybot = ytop + height

            for row in range(5):
                xtop = x + (width + xspace) * row
                xbot = xtop + width
                
                self.levelButttons[(xtop, ytop, xbot, ybot)] = level
                level += 1

    def clickedButton(self): 
        x, y = self.mousex, self.mousey
        if self.startMode == 0: #startup mode
            playX1, playY1, playX2, playY2 = self.playButton
            instX1, instY1, instX2, instY2 = self.instructButton
            levelX1, levelY1, levelX2, levelY2 = self.levelButton
            if playX1 <= x <= playX2 and playY1 <= y <= playY2:
                return "play"
            elif instX1 <= x <= instX2 and instY1 <= y <= instY2:
                return "instructions"
            elif levelX1 <= x <= levelX2 and levelY1 <= y <= levelY2:
                self.startMode = 5
                return "select level"
        elif 1 <= self.startMode < 4: #instructions mode
            playX1, playY1, playX2, playY2 = self.instructPlayButton
            backX1, backY1, backX2, backY2 = self.backButton
            nextX1, nextY1, nextX2, nextY2 = self.nextButton
            if playX1 <= x <= playX2 and playY1 <= y <= playY2:
                return "play"
            elif backX1 <= x <= backX2 and backY1 <= y <= backY2:
                self.startMode -= 1
                return "instructions" if self.startMode != 0 else "home"
            elif nextX1 <= x <= nextX2 and nextY1 <= y <= nextY2:
                self.startMode = (self.startMode + 1) % 4
                return "instructions" if self.startMode != 0 else "home"
        elif self.startMode == 5: #select level mode
            homeX1, homeY1, homeX2, homeY2 = self.homeButton
            randomX1, randomY1, randomX2, randomY2 = self.randomButton
            if homeX1 <= x <= homeX2 and homeY1 <= y <= homeY2:
                self.startMode = 0
                return "home"
            elif randomX1 <= x <= randomX2 and randomY1 <= y <= randomY2:
                self.level = random.choice(range(0,14))
                return "random level"
            else:
                for button in self.levelButttons:
                    x1, y1, x2, y2 = button
                    if x1 <= x <= x2 and y1 <= y <= y2:
                        self.level = self.levelButttons[button]
                        return "level selected"

    def update(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                return 1
            elif event.type == MOUSEBUTTONUP:
                self.mousex, self.mousey = event.pos
                button = self.clickedButton()
                if button != None: 
                    self.buttonPressed = button
                if self.buttonPressed != None:
                    if self.startMode == 0 and button == "instructions":
                        self.startMode = 1
                    return self.buttonPressed
       
        if self.buttonPressed == None:
            if self.startMode == 0: return "home"
            else: return None
        else: return self.buttonPressed


    def displayStartPage(self, screen):
        if 0 <= self.frameCount < 20: start = self.startPage[0]
        elif 20 <= self.frameCount < 40: start = self.startPage[1]
        else: start = self.startPage[2]
        self.frameCount = (self.frameCount + 1) % 60
        
        screen.blit(start, (0,0))
        pygame.display.flip()

    def displayInstructions(self, screen):
        screen.blit(self.instructions[self.startMode-1], (0,0))
        pygame.display.flip()

    def displayLevels(self, screen):
        screen.blit(self.levelsPage, (0,0))
        pygame.display.flip()        
