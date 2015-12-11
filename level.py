"""
level.py
created by Rachel Kim (rhkim)
 for 15-112 F15 Term Project

loads level using helper/data files from https://pyweek.org/e/Cthulhu32_v2/
"""
import pygame, os
from helper import *
class Level:
	def __init__(self,level):
		self.groundSurface = None
		self.titleSurface = 0
		self.roomTitle = ""
		self.groundData = [] #ground data
		
		self.level = level

		self.levelRows = self.levelCols = 0
		self.playerStartRow = self.playerStartCol = 0
		self.targetRow = self.targetCol = 0
		self.coinPos = self.keyPos = self.lockPos = (None, None)
		self.switches = set()
		self.portals = set()
		self.meltedIce = set()

		self.walls = set()
		self.tileSize = 32

		self.iceNum = 1
		self.levelMin = self.levelSec = 0

		self.playerWins = False
		self.hasKey = False

		water1, null = load_image("water.gif")
		water2, null = load_image("water2.gif")
		self.water = [water1, water2]
		self.frameCount = 0

	def getGroundData(self):
		if self.level < 10: fullname = os.path.join('levels', 'level0'+str(self.level)+'.txt')
		else: fullname = os.path.join('levels', 'level'+str(self.level)+'.txt')
		try: #if you can load the file... otherwise go to line 89
			openLevel = open(fullname)
			self.roomTitle = openLevel.readline().strip()
			line = openLevel.readline().strip()
			if line == "Ground":
			    line = openLevel.readline().strip()
			    while line != "Time":
			        self.groundData.append(line)
			        line = openLevel.readline().strip()
			
			line = openLevel.readline().strip()
			time = []
			for num in line.split(" "): time.append(int(num))
			self.levelMin, self.levelSec = time[0], time[1]
			openLevel.close() # CLOSE IT UP

			self.levelRows, self.levelCols = len(self.groundData), len(self.groundData[0])

		except: #if you cannot load the file... there are no more leves; player wins!
			self.playerWins = True

	def makeGroundSurface(self):
		# make a ground surface
		self.groundSurface = pygame.Surface((self.levelCols*self.tileSize,self.levelRows*self.tileSize))
		self.groundSurface.fill((125,125,125))
		# make a tile surface and fill it with transparancy
		self.tileSurface = pygame.Surface((self.levelCols*self.tileSize,self.levelRows*self.tileSize))
		self.tileSurface.set_colorkey((0,255,0))
		self.tileSurface.fill((0,255,0))# setup tiles to blit

	def blitTiles(self):
		# setup tiles to blit
		#0 background; 1 wall; 2 ice; 3 water
		#P player; T target; C coins; S switch
		print(self.groundData)
		for row in range(self.levelRows):
			for col in range(self.levelCols):
				curTile = self.groundData[row][col]
				try:
					curTile = int(curTile)
					if curTile == 0: #background
						tile, null = load_image("background.gif")
					elif curTile == 1: #wall
						self.walls.add((row,col))
						tile, null = load_image("wall.gif")
					elif curTile == 2: #ice
						tile, null = load_image("ice.gif")
						self.iceNum += 1
				except:
					if curTile == 'T': #target
						self.targetRow, self.targetCol = row, col
						tile, null = load_image("target.gif")
					elif curTile == 'S': #switch ("double ice")
						self.switches.add((row,col))
						tile, null = load_image("switch.gif")
						self.iceNum += 2
					elif curTile == 'L': #lock
						self.lockPos = (row, col)
						tile, null = load_image("lock.gif")
					elif curTile == 'p': #portal
						self.portals.add((row, col))
						tile, null = load_image("portal.gif")
						self.iceNum += 2							
					elif curTile == 'P': #player
						self.playerStartRow, self.playerStartCol = row, col
						tile, null = load_image("ice.gif")
					elif curTile == 'C': #coin
						self.coinPos = (row, col)
						tile, null = load_image("coin.gif")
					elif curTile == 'K': #key
						self.hasKey = True
						self.keyPos = (row, col)
						tile, null = load_image("key.gif")

				self.groundSurface.blit(tile, (col*self.tileSize, row*self.tileSize))

		
	def loadLevel(self):
		self.getGroundData()
		self.makeGroundSurface()
		self.blitTiles()	
		
	def meltIce(self,row,col):
		self.meltedIce.add((row,col))

	def turnToIce(self,row,col):
		tile, null = load_image("ice.gif")
		self.groundSurface.blit(tile, (col*self.tileSize, row*self.tileSize))

	def unlockDoor(self):
		row, col = self.lockPos
		self.turnToIce(row, col)
			
	def drawMeltedIce(self):
		for tile in self.meltedIce:
			row, col = tile
			if self.frameCount < 20: water = self.water[0]
			else: water = self.water[1]
			self.groundSurface.blit(water, (col*self.tileSize, row*self.tileSize))
			self.frameCount = (self.frameCount + 1) % 20

	def draw(self, screen):
		if self.groundSurface != None:
			self.drawMeltedIce()
			screen.blit(self.groundSurface, (0,self.tileSize))
