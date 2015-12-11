"""
game.py
created by Rachel Kim (rhkim)
 for 15-112 F15 Term Project
"""
import pygame, sys
from scene import Scene
from player import Player
from startup import StartUp
from gameOver import GameOver
from audio import *
from helper import *
	
class Game(object):
	def __init__(self, width=608, height=544):
		pygame.init()
		self.width = width
		self.height = height
		self.screen = pygame.display.set_mode((self.width, self.height))
		pygame.display.set_caption("Thin Ice")

		self.clock = pygame.time.Clock()
		self.player = Player()
		self.gameOver = False
		self.gameMode = 0 #0-menu; 1-play mode; 2-game over; 3-game over bc player won!; 4-timeout
		self.finalScore = 0
		self.level = 0

		self.quit = False

	def exit(self,quit=False):
		if not quit: return False
		else: return True

	def runStart(self):
		startscreen = StartUp()
		playMusic("intro")

		while self.gameMode == 0:
			self.clock.tick(100)
			update = startscreen.update()
			if update == 1:
				self.quit = True
				return False
			elif update == "play":
				self.gameMode = 1
			elif update == "home":
				startscreen.displayStartPage(self.screen)
			elif update == "instructions":
				startscreen.displayInstructions(self.screen)
			elif update == "select level":
				startscreen.displayLevels(self.screen)
			elif update == "random level" or update == "level selected":
				self.level = startscreen.level-1
				self.gameMode = 1
			


	def playGame(self):		
		gameScene = Scene(self.player, self.level) # start at level 0; gameScene immediately calls level up to start at level 1
		while self.gameMode == 1:
		    self.clock.tick(1090)
		    
		    #background music
		    curlevel = gameScene.levelcnt
		    if curlevel != self.level: #when level up
		    	self.level = curlevel
		    	playMusic("game",curlevel)    
		    
		    #update the gamescene
		    update = gameScene.update()
		    if update == 1: #pressed exit button
		    	self.quit = True
		    	return False

		    elif update == 2: #pressed the restart button
		    	self.gameMode = 0
		    	return True
		    	
		    elif gameScene.gameOver:
    			self.finalScore = gameScene.score
		    	playerWins = gameScene.playerWins
		    	timeOut = gameScene.timeOut
		    	if timeOut: self.gameMode = 4
		    	elif playerWins: self.gameMode = 3
		    	else: self.gameMode = 2
		    	break

		    elif not gameScene.gameOver:
		    	gameScene.display(self.screen)


	def runGameOver(self):
		gameover = GameOver(self.gameMode, self.finalScore)
		gameover.display(self.screen)
		
		if self.gameMode == 2: playMusic("you lose")
		elif self.gameMode == 3: playMusic("you win")
		elif self.gameMode == 4: playMusic("time out")

		while self.gameMode >= 2:
			update = gameover.update()
			if update == 1:
				self.quit = True
				return False
			elif update == "play again":
				return True	
			elif update == "show scores":
				gameover.displayScores(self.screen)
		return False

	def Run(self):
		start = self.runStart()
		if start != None: return start
		play = self.playGame()
		if play != None: return play
		gameover = self.runGameOver()
		return gameover
 		

newGame = Game()
while not newGame.quit and newGame.Run():
	newGame = Game()

pygame.quit()
sys.exit()
