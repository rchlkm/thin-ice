"""
highscore.py
created by Rachel Kim (rhkim)
 for 15-112 F15 Term Proje

reads highscore.txt file 
compares current game's score with the high score data stored
"""
import os
def getHighScore():
	try:
		scoretxt = open("highscore.txt")
		highscore = int(scoretxt.read())
		scoretxt.close()
	except:
		highscore = 0
		print("There is no high score")
	return highscore

def saveHighScore(newHighScore):
    try:
        # Write the file to disk
        highscoretxt = open("highscore.txt", "w")
        highscoretxt.write(str(newHighScore))
        highscoretxt.close()
    except:
        print("Unable to save the high score.")

