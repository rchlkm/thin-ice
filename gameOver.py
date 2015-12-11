"""
gameOver.py
created by Rachel Kim (rhkim)
 for 15-112 F15 Term Project

handles when the game is over

"""

import pygame, os
from highscore import *
from helper import *
class GameOver:

    def __init__(self, gameOverType, finalScore):
        self.gameOverType = gameOverType
        self.mousex = self.mousey = None
        self.tryAgain = (172, 246, 472, 306)
        self.scores = (222, 330, 423, 380)
        self.playAgain = (172, 390, 472, 454)
        self.gameOver,null = load_image('playerLoses.gif') #2
        self.playerWins,null = load_image('playerWins.gif') #3
        self.timeOut,null = load_image('playerLoses2.gif') #4
        self.scoresPage,null = load_image('scores.gif')
        self.showScores = False

        self.finalScore = finalScore
        self.highScore = getHighScore()
        self.beatScore = self.beatHighScore()

    def clickedButton(self):
        x, y = self.mousex, self.mousey
        if self.showScores == False:
            tryX1, tryY1, tryX2, tryY2 = self.tryAgain
            scoresX1, scoresY1, scoresX2, scoresY2 = self.scores
            if tryX1 <= x <= tryX2 and tryY1 <= y <= tryY2:
                return "play again"
            elif scoresX1 <= x <= scoresX2 and scoresY1 <= y <= scoresY2:
                self.showScores = True
                return "show scores"
        else:
            playX1, playY1, playX2, playY2 = self.playAgain
            if playX1 <= x <= playX2 and playY1 <= y <= playY2:
                return "play again"        
        return None

    def update(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                return 1
            
            elif event.type == MOUSEBUTTONUP:
                self.mousex, self.mousey = event.pos
                button = self.clickedButton()
                return button
        return 0

    def beatHighScore(self):
        if self.finalScore >= self.highScore:
            saveHighScore(self.finalScore)
            self.highScore = self.finalScore
            return True
        return False

    def display(self, screen):
        image = None
        if self.gameOverType == 2:
            image = self.gameOver
        elif self.gameOverType == 3:
            image = self.playerWins
        elif self.gameOverType == 4:
            image = self.timeOut
        if image != None:
            screen.blit(image, (0,0))
            pygame.display.flip()

    def displayScores(self, screen):
        screen.blit(self.scoresPage, (0,0))

        font = pygame.font.Font("Krungthep.ttf", 30)        
        #your score
        yourscore = font.render(str(self.finalScore), True, (70, 121, 203))
        x, y = 44, 212
        screen.blit(yourscore, [x, y])  

        #best score
        score = str(self.highScore)
        x, y = 375, 212
        spaces = 10 - len(score)
        x += spaces * 18
        bestscore = font.render(score, True, (70, 121, 203))      
        screen.blit(bestscore, [x, y])  

        #message
        font = pygame.font.Font("Krungthep.ttf", 35)
        font.set_bold(True)
        if self.beatScore: 
            txt = "New High Score!"
            x, y = 145, 300
        else: 
            txt = "Try Again Next Time?"
            x, y = 80, 300
        message = font.render(txt, True, (70, 121, 203))
        screen.blit(message, [x, y])  
        
        pygame.display.flip()
