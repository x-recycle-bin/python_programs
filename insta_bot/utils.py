'''
	@file: utils.py

	@desc: Some utility functions

'''

import time
from datetime import datetime
import constants as CONSTANTS

def logMessage(message):

	currentTime = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
	file = open(CONSTANTS.LOG_FILE, "a")
	dataToWrite = "(" + currentTime + "): " + message + "\n\n"
	file.write(dataToWrite)
	file.close()

'''
	Reads a list of strings from the input
	file, each of which are on separate lines
	and returns them as a list

'''

def getDataFromFile(fileName):

	with open(fileName) as f:
		content = f.readlines()

	# remove whitespace characters like `\n` at the end of each line
	content = [x.strip() for x in content]
	return content

