"""
scene.py
created by Rachel Kim (rhkim)
 for 15-112 F15 Term Project

draws and updates the game when it is in play mode
"""

import pygame, os
from level import Level
from countdown import Countdown
from helper import *
BLUE = (9, 77, 191)
RED = (231, 85, 80)
class Scene:
	def __init__(self, player, levelcnt):
		self.levelcnt = levelcnt

		self.player = player
		self.gameOver = False
		self.timeOut = False

		self.score = 0
		self.levelUp()

		self.dontMeltLastPos = False #True if the last position had a switch
		self.iceLastPos = False #True if last position had a portal

	def levelUp(self):
		#set the current level
		self.levelcnt += 1
		self.curLevel = Level(self.levelcnt) #create a new level

		self.player.__init__()
		#load level
		self.curLevel.loadLevel()
		self.levelRows, self.levelCols = self.curLevel.levelRows, self.curLevel.levelCols
		self.playerStartRow, self.playerStartCol = self.curLevel.playerStartRow, self.curLevel.playerStartCol
		self.targetRow, self.targetCol = self.curLevel.targetRow, self.curLevel.targetCol
		self.walls = self.curLevel.walls
		self.iceNum = self.curLevel.iceNum
		self.switches = self.curLevel.switches
		self.levelMin, self.levelSec = self.curLevel.levelMin, self.curLevel.levelSec
		self.countdown = Countdown(self.levelMin, self.levelSec)
		self.iceMelted = 0
		self.keyObtained = False

		#level loaded; set player data
		self.player.setPos(self.playerStartRow, self.playerStartCol)
		self.player.setBoundaries(self.walls)
		self.player.setTargetPos(self.targetRow, self.targetCol)
		if self.curLevel.hasKey: self.player.setDoorLock(self.curLevel.lockPos)
	
	def meltOldPos(self, oldRow, oldCol):
		#checks if the last position was a switch
		#if it was a switch, change boolean
		#if it was not a switch, melt the old position
		if self.dontMeltLastPos == False:
			self.curLevel.meltIce(oldRow,oldCol)
			self.iceMelted += 1
		else: self.dontMeltLastPos = False

	def updateAlivePlayer(self):
		for event in pygame.event.get():
			if event.type == QUIT: return 1
			elif event.type == MOUSEBUTTONUP:
				x, y = event.pos
				restartX1, restartY1, restartX2, restartY2 = (4,515,105,538)
				if restartX1 <= x <= restartX2 and restartY1 <= y <= restartY2: return 2

			elif event.type == KEYDOWN:
				if event.key == K_RIGHT: self.player.move(0,+1)
				elif event.key == K_LEFT: self.player.move(0,-1)
				elif event.key == K_UP: self.player.move(-1,0)
				elif event.key == K_DOWN: self.player.move(+1,0)
				else: return 0 #break for loop if a different key pressed
					
				oldRow, oldCol = self.player.getOldPos()
				curRow, curCol = self.player.getCurPos()
				if (oldRow != None and oldCol != None) and (oldRow != curRow or oldCol != curCol):
					#only melt ice and increase score when the player has made a valid move
					coinRow, coinCol = self.curLevel.coinPos
					keyRow, keyCol = self.curLevel.keyPos
					lockRow, lockCol = self.curLevel.lockPos
					pos = (curRow, curCol)
					if pos in self.switches:
						self.score += 10
						self.curLevel.turnToIce(curRow,curCol) #once stepped on a switch, it becomes ice
						self.switches.remove(pos) #switch no longer exists		
						self.player.visited.remove(pos) #player can step on switch tiles twice
						self.meltOldPos(oldRow,oldCol) 
						self.dontMeltLastPos = True #if "cur" pos was a switch, it was turned into ice; do not melt it
						break

					elif pos in self.curLevel.portals:
						self.score += 10

						for portal in self.curLevel.portals:
							if pos != portal:
								newRow, newCol = portal

						self.curLevel.turnToIce(curRow,curCol)
						self.player.setPos(newRow, newCol)
						self.player.visited.remove(pos)
						self.curLevel.portals.clear()
						self.iceLastPos = True 
						break
					
					elif self.iceLastPos: #if the last position was a portal, scene should turn last pos to
						self.curLevel.turnToIce(oldRow,oldCol)
						self.iceLastPos = False
						break

					elif (coinRow != None and coinCol != None) and (coinRow == curRow and coinCol == curCol):
						self.score += 50 #bonus points bc hit a coin

					elif self.curLevel.hasKey: 
						if keyRow == curRow and keyCol == curCol:
							self.score += 20
							self.keyObtained = self.player.keyObtained = True
						elif lockRow == curRow and lockCol == curCol:
							if self.keyObtained: 
								self.score += 20
								self.curLevel.unlockDoor()
							else: print("key not obtained; cannot unlock door")

					self.score += 8 #not a special case tile		
					self.meltOldPos(oldRow,oldCol)
					

	def update(self):
		self.playerState = self.player.getPlayerState()
		self.playerWins = self.curLevel.playerWins
		timerUpdate = self.countdown.update()

		if not self.playerWins and timerUpdate == "game over": 
			self.timeOut = self.gameOver = True
			
		elif self.playerWins: 
			self.gameOver = True
		
		elif self.playerState == 1: #alive
			return self.updateAlivePlayer()

		elif self.playerState == 2: #reached target
			if self.iceMelted == self.iceNum:
				self.score += self.iceNum*2 #bonus point for melting all ice on that level
			self.levelUp()

		elif self.playerState == 0: #dead
			row,col = self.player.getDiedPos()
			self.curLevel.meltIce(row,col)
			self.gameOver = True
			pygame.time.delay(600)		
		return 0

	def drawText(self,screen):
		font = pygame.font.Font("Krungthep.ttf", 20)
		font.set_bold(True)
		
		#score
		score = font.render("score: %d" % self.score, True, BLUE)
		screen.blit(score, [445, 515])	

		#level
		level = font.render("level: %d" % self.levelcnt, True, BLUE)
		screen.blit(level, [5, 5])

		#ice block count
		iceMelted = str(self.iceMelted)
		if len(iceMelted) == 1: iceMelted = " " + iceMelted
		blocktxt = iceMelted + "/" + str(self.iceNum)
		blocks = font.render(blocktxt, True, BLUE)
		screen.blit(blocks, [520, 5])

		#key needed
		self.drawKeyText(screen)

	def drawKeyText(self, screen):
		font = pygame.font.Font("Krungthep.ttf", 15)
		font.set_bold(True)
		key = font.render("KEY: ", True, BLUE)
		screen.blit(key, [222, 518])
		if self.curLevel.hasKey: #needs key
			if self.keyObtained: status = "obtained"
			else: status = "unobtained"
		else: #does not need key
			status = "unavailable"
		keytxt = "KEY: " + status
		key = font.render(status, True, RED)
		screen.blit(key, [265, 518])
            
	def display(self, screen):		
		BG, null = load_image("base.gif")
		screen.blit(BG, (0,0))
	
		self.drawText(screen)
		self.countdown.draw(screen)

		self.curLevel.draw(screen)
		self.player.draw(screen)

		pygame.display.flip()

