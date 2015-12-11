"""
player.py
created by Rachel Kim (rhkim)
 for 15-112 F15 Term Project

draws and moves the character
"""
import pygame
from helper import *

class Player(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image,self.rect = load_image("puffle.gif",-1)
		self.playerState = 1 #0-died, 1-alive, 2-win, 3-timeout

		self.row = self.col = None
		self.oldRow = self.oldCol = None
		self.targetRow = self.targetCol = None
		self.diedRow = self.diedCol = None
		self.posx = self.posy = None
		self.hasLock = self.keyObtained = False
		
		self.tileSize = 32
		self.walls = None
		self.visited = set()
		

	def setBounds(self):
		self.posy += self.tileSize

	def setPos(self, row, col):
		self.row = row
		self.col = col
		self.visited.add((row,col))

		self.posx = col * self.tileSize
		self.posy = row * self.tileSize
		self.setBounds()
		
	def setBoundaries(self,walls):
		self.walls = walls

	def setDoorLock(self, lockPos):
		self.hasLock = True
		self.lockPos = lockPos


	def setTargetPos(self, targetRow, targetCol):
		self.targetRow = targetRow
		self.targetCol = targetCol

	def playerAtTarget(self, row, col):
		if row == self.targetRow and col == self.targetCol:
			return True
		return False

	def move(self,drow,dcol):
		self.oldRow, self.oldCol = self.row, self.col
		newRow, newCol = self.row + drow, self.col + dcol

		if (newRow,newCol) not in self.walls:
			if (self.hasLock and (newRow,newCol) == self.lockPos and not self.keyObtained):
				print("cannot make move")
				pass
		
			else:
				self.movePlayer(newRow, newCol, drow, dcol)
				
		else: print("not a valid move")	

	def movePlayer(self, newRow, newCol, drow, dcol):
		self.row += drow
		self.col += dcol
		
		dx, dy = dcol * self.tileSize, drow * self.tileSize

		self.posx += dx
		self.posy += dy		

		if (newRow,newCol) in self.visited:
			self.diedRow, self.diedCol = newRow, newCol
			print("DIED",(self.diedRow,self.diedCol))
			self.playerState = 0

		else: #player hasn't visited the new position
			self.visited.add((newRow, newCol))
			if self.playerAtTarget(newRow,newCol):
				self.playerState = 2

	def undoMove(self, row, col):
		self.visited.remove(row,col)

	def getOldPos(self):
		return self.oldRow, self.oldCol

	def getCurPos(self):
		return self.row, self.col

	def getDiedPos(self):
		return self.diedRow, self.diedCol

	def getPlayerState(self):
		return self.playerState

	def setPlayerState(self, state):
		self.playerState = state

	def draw(self, screen):
		screen.blit(self.image, (self.posx,self.posy))


