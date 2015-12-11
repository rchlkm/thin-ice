"""
main.py
created by Rachel Kim (rhkim)
 for 15-112 F15 Term Project

creates game, inifinitely creates newGame 
until player stops pressing "play again" or "try again 
once in the game over mode
"""
import os, pygame
from pygame.locals import *

from game import Game

def main():	
	newGame = Game()
	while not newGame.quit and newGame.Run():
		newGame = Game()

	pygame.quit()
	sys.exit()