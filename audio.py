"""
audio.py
created by Rachel Kim (rhkim)
 for 15-112 F15 Term Project

gets the music files and plays the corresponding file to the gameMode
"""

from helper import *
easy = ["play1.wav", "play2.wav", "play3.wav"]
hard = ["play4.wav", "play5.wav", "play6.wav"]

def getMusic(gameMode, level):
	if gameMode == "intro": music = "introMusic.wav"
	elif gameMode == "you lose": music = "youlose.wav"
	elif gameMode == "you win": music = "youwin.wav"
	elif gameMode == "time out": music = "youlose2.wav"
	elif gameMode == "game":
		index = (level-1) % 3 
		if level < 7: music = easy[index]
		else: music = hard[index]
	return music


def playMusic(gameMode, level=None):
	musicName = getMusic(gameMode,level)
	load_music(musicName)
	pygame.mixer.music.play(-1)

