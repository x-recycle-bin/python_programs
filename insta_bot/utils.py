'''
	@file: utils.py

	@desc: Some utility functions

'''

import time
import constants as CONSTANTS

# Maintain a log of the "likes" we perform
def logOperation(usernameOfPhoto, photosLiked):

	currentTime = time.strftime("%Y-%m-%d %H:%M:%S", gmtime())
	file = open(CONSTANTS.LOG_FILE, "a")
	dataToWrite = "(" + currentTime + "): " + "Liked photo of user: " + usernameOfPhoto + " (PhotosLiked: " + photosLiked + ")\n\n"
	file.write(dataToWrite)
	file.close()

def logError(errorString):

	currentTime = time.strftime("%Y-%m-%d %H:%M:%S", gmtime())
	file = open(CONSTANTS.LOG_FILE, "a")
	dataToWrite = "(" + currentTime + "): " + "Error occurred\n" + errorString + "\n\n"
	file.write(dataToWrite)
	file.close()