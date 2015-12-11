"""
ountdown.py
created by Rachel Kim (rhkim)
 for 15-112 F15 Term Project

creates a countdown timer
"""
import pygame

class Countdown:
	def __init__(self, minutes, seconds, milliseconds=0):
		self.time = [minutes, seconds, milliseconds]
	

	def update(self):
		self.time[2] -= 1
		if self.time[2] < 0: #milliseconds
			self.time[2] = 99
			self.time[1] -= 1

			if self.time[1] < 0: #seoncds
			    self.time[1] = 59
			    self.time[0] -= 1

			    if self.time[0] < 0: #minutes
			        self.time = [0,0,0]
			        return "game over"

	def draw(self, screen):
		minutes = str(self.time[0])
		if len(minutes) == 1: minutes = "0" + minutes
		seconds = str(self.time[1])
		if len(seconds) == 1: seconds = "0" + seconds
		milliseconds = str(self.time[2])
		if len(milliseconds) == 1: milliseconds = "0" + milliseconds
		time = minutes + ":" + seconds + ":" + milliseconds

		font = pygame.font.Font("Krungthep.ttf", 28)		

		#timer
		timetxt = font.render(time, True, (9,77,191))
		x, y = 240, 1
		screen.blit(timetxt, [x, y])	

