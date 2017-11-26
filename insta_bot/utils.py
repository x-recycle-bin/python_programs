'''
	@file: utils.py

	@desc: Some utility functions

'''

import time
from datetime import datetime
import constants as CONSTANTS

# Maintain a log of the "likes" we perform
def logOperation(usernameOfPhoto, photosLiked):

	currentTime = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
	file = open(CONSTANTS.LOG_FILE, "a")
	dataToWrite = "(" + currentTime + "): " + "Liked photo of user: " + usernameOfPhoto + " (PhotosLiked: " + str(photosLiked) + ")\n\n"
	file.write(dataToWrite)
	file.close()

def logError(errorString):

	currentTime = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
	file = open(CONSTANTS.LOG_FILE, "a")
	dataToWrite = "(" + currentTime + "): " + "Error occurred\n" + errorString + "\n\n"
	file.write(dataToWrite)
	file.close()

def logMessage(message):

	currentTime = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
	file = open(CONSTANTS.LOG_FILE, "a")
	dataToWrite = "(" + currentTime + "): " + message + "\n\n"
	file.write(dataToWrite)
	file.close()