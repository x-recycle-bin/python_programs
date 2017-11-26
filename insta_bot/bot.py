'''
	@file: bot.py

	@desc: Contains functions specific to running the bot

'''

import time
import re
import random
import os.path
from bs4 import BeautifulSoup as webcrawl
import constants as CONSTANTS
import parser
import utils

# Determines whether we should like the photo or not
def shouldlikePhoto(photoContainer):

	# Find whether we have already liked the photo or not
	likeStatusContent = str(webcrawl(photoContainer, "html.parser").contents[2].contents[0].contents[0])
	return bool(re.search(CONSTANTS.WHITE_LIKE_BUTTON_CLASS, likeStatusContent))

# Determines whether we should save the photo or not
def shouldArchiveThePhoto(photoContainer, usernameOfPhoto, archiveUsers):

	if usernameOfPhoto in archiveUsers:
		# Find whether we have already saved the photo or not
		archiveStatusContent = str(webcrawl(photoContainer, "html.parser").contents[2].contents[0].contents[2])
		return bool(re.search(CONSTANTS.WHITE_ARCHIVE_BUTTON_CLASS, archiveStatusContent))
	else:
		return False

# Interacts with photos on the given page
def interactWithPhotos(driver, interactionsTillNow, blackListedUsers, archiveUsers):

	interactionCount = 0

	# Find all photos in the current page
	# photolist = driver.find_elements_by_css_selector(articleClassSelector)
	photolist = driver.find_elements_by_tag_name("article")

	# Find like and archive button classes
	optionList = webcrawl(photolist[0].get_attribute('innerHTML'), "html.parser").contents[2].contents[0].findAll("a")
	
	likeButtonClass = str(optionList[0].attrs["class"])
	archiveButtonClass = str(optionList[2].attrs["class"])

	likeButtonClassSelector = parser.concatenate2(likeButtonClass)
	archiveButtonClassSelector = parser.concatenate2(archiveButtonClass)

	likeButtons = driver.find_elements_by_css_selector(likeButtonClassSelector)
	archiveButtons = driver.find_elements_by_css_selector(archiveButtonClassSelector)

	for i in range(0, len(photolist)):

		# Return, if we reached max interactions allowed
		if (interactionsTillNow + interactionCount) == CONSTANTS.MAX_INTERACTIONS:
			break

		# Find the username to which the photo belongs
		photoContainer = photolist[i].get_attribute('innerHTML')
		usernameOfPhoto = str(webcrawl(photoContainer, "html.parser").header.contents[1].contents[0].contents[0].contents[0].contents[0])

		# Don't interact with black listed users
		if usernameOfPhoto in blackListedUsers:
			utils.logMessage("User: " + usernameOfPhoto + " is blacklisted")
			continue

		shouldLike = shouldlikePhoto(photoContainer)
		shouldArchive = shouldArchiveThePhoto(photoContainer, usernameOfPhoto, archiveUsers)

		if shouldLike:
			likeButtons[i].click()
			utils.logMessage("Liked photo of user: " + usernameOfPhoto)

		if shouldArchive:
			archiveButtons[i].click()
			utils.logMessage("Saved photo of user: " + usernameOfPhoto)

		# Increment only if you have interacted with the photo in some way
		if shouldLike or shouldArchive:
			interactionCount = interactionCount + 1
			utils.logMessage("Interaction Count: " + str(interactionCount + interactionsTillNow))

	return interactionCount

# Watches stories
def watchStories(driver):

	pageData = driver.find_element_by_tag_name("body").get_attribute('innerHTML')
	storiesButtonClass = parser.findStoriesButton(str(webcrawl(pageData, "html.parser")))

	if parser.containsSpaces(storiesButtonClass):
		storiesButtonClassSelector = parser.concatenate2(storiesButtonClass)
		driver.find_elements_by_css_selector(storiesButtonClassSelector).click()
	else:
		driver.find_element_by_class_name(storiesButtonClass).click()

# Driver function for interactWithPhotos() and watchStories() (See README for understanding this)
def runBot(webPageData, driver):

	# Each image is wrapped with <article> (Get its class)
	scrollHeight = driver.find_elements_by_tag_name("article")[0].get_attribute("scrollHeight")

	'''
		For achieving the scrolling effect (so that new images
		get loaded), we need to run javascript with the help of
		selenium

	'''
	scrollJSScript = "window.scrollBy(0, " + scrollHeight + ");"

	# Get the users whom you don't want to interact with
	blackListedUsers = []
	blackListFileExists = os.path.isfile(CONSTANTS.BLACK_LIST_FILE)
	if blackListFileExists:
		blackListedUsers = utils.getDataFromFile(CONSTANTS.BLACK_LIST_FILE)

	archiveUsers = []
	archiveListFileExists = os.path.isfile(CONSTANTS.ARCHIVE_LIST_FILE)
	if archiveListFileExists:
		archiveUsers = utils.getDataFromFile(CONSTANTS.ARCHIVE_LIST_FILE)

	# At max, interacts with top k photos (where k = CONSTANTS.MAX_INTERACTIONS)
	totalInteractionCount = 0

	# Scroll only 100 times at max
	for iterations in range(0,100):

		interactionCount = interactWithPhotos(driver, totalInteractionCount, blackListedUsers, archiveUsers)
		totalInteractionCount = totalInteractionCount + interactionCount
		if totalInteractionCount == CONSTANTS.MAX_INTERACTIONS:
			break
		else:
			# Scroll the page to get new photos
			driver.execute_script(scrollJSScript)
			# Wait for the page to load
			time.sleep(3 * CONSTANTS.WAIT_TIME)

	# Watch the stories now
	utils.logMessage("Started watching stories")
	watchStories(driver)
	time.sleep(10 * CONSTANTS.WAIT_TIME)
	utils.logMessage("Stopped watching stories")




