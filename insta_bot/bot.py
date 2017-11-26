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

# Determines whether we should comment on the photo or not
def shouldCommentOnPhoto(shouldLike, usernameOfPhoto, commentUsers):

	'''
		Here, we don't have a way to detect whether we have
		already commented the photo or not.

		We use a small heuristic to determine whether we
		have commented or not. i.e., we check whether we
		have already liked the photo or not, if yes,
		then it means we have already commented, if no,
		i.e. we are yet to like the photo, then we'll
		assume that we have not yet commented.

		Note: We can find out whether we have commented or
		not by searching the comments in the photo. But
		if there are more no:of comments then it will become
		a problem in parsing. We defer this until next
		version

	'''

	if usernameOfPhoto in commentUsers:
		if shouldLike:
			return True
		else:
			return False
	else:
		return False

# Determines whether we should save the photo or not
def shouldArchiveThePhoto(photoContainer, usernameOfPhoto, archiveUsers):

	if usernameOfPhoto in archiveUsers:
		# Find whether we have already saved the photo or not
		archiveStatusContent = str(webcrawl(photoContainer, "html.parser").contents[2].contents[0].contents[2])
		return bool(re.search(CONSTANTS.WHITE_ARCHIVE_BUTTON_CLASS, archiveStatusContent))
	else:
		return False

'''
	Given a comment button to click on, this function will
	post a sampleComment on the section which appears, as the comment
	button is clicked

'''
def postComment(driver, photoContainer, sampleComment, index):

	# Find the form which corresponds to posting comment
	formTag = webcrawl(photoContainer, "html.parser").contents[2].contents[4].contents[0]

	# Find the class namaes
	formTagClassName = formTag.attrs["class"][0]
	textAreaClassName = formTag.contents[0].attrs["class"][0]

	# Write the comment
	driver.find_elements_by_class_name(textAreaClassName)[index].send_keys(sampleComment)
	time.sleep(WAIT_TIME * 2)

	# Submit it
	driver.find_elements_by_class_name(formTagClassName)[index].submit()
	time.sleep(WAIT_TIME * 2)


# Interacts with photos on the given page
def interactWithPhotos(driver, articleClassSelector, interactionsTillNow, blackListedUsers, \
						commentUsers, sampleComments, archiveUsers):

	interactionCount = 0

	# Find all photos in the current page
	photolist = driver.find_elements_by_css_selector(articleClassSelector)

	# Find like, comment and archive button classes
	optionList = webcrawl(photolist[0].get_attribute('innerHTML'), "html.parser").contents[2].contents[0].findAll("a")
	
	likeButtonClass = str(optionList[0].attrs["class"])
	commentButtonClass = str(optionList[1].attrs["class"])
	archiveButtonClass = str(optionList[2].attrs["class"])

	likeButtonClassSelector = parser.concatenate2(likeButtonClass)
	commentButtonClassSelector = parser.concatenate2(commentButtonClass)
	archiveButtonClassSelector = parser.concatenate2(archiveButtonClass)

	likeButtons = driver.find_elements_by_css_selector(likeButtonClassSelector)
	commentButtons = driver.find_elements_by_css_selector(commentButtonClassSelector)
	archiveButtons = driver.find_elements_by_css_selector(archiveButtonClassSelector)

	'''
		If users have disabled comments, or there is any error in the previous statements
		where we find the like, comment and archive buttons, then return 0 to caller.

		We can solve the problem when users disable comments in the next version of the
		bot.

	'''
	if (len(likeButtons) != len(commentButtons)) and (len(commentButtons) != len(archiveButtons)):
		utils.logMessage("List of likes(" + len(likeButtons) + "), comments(" + len(commentButtons) + ")," + \
							" and archive(" + len(archiveButtons) + ") buttons are not same on this webpage")
		return interactionCount

	for button in commentButtons:
		print(str(button.get_attribute('innerHTML')))

	# Open all comment sections by clicking on comment buttons
	itr = 0
	for button in commentButtons:
		print("Clicking on button of username: " + str(itr))
		button.click()
		print("Clicked on button of username: " + str(itr))
		itr = itr + 1

	for i in range(0, len(photolist)):

		# Return, if we reached max interactions allowed
		if (interactionsTillNow + interactionCount) == CONSTANTS.MAX_INTERACTIONS:
			break

		# Find the username to which the photo belongs
		photoContainer = photolist[i].get_attribute('innerHTML')
		usernameOfPhoto = str(webcrawl(photoContainer, "html.parser").header.contents[1].contents[0].contents[0].contents[0].contents[0])
		print("Username: " + usernameOfPhoto + " index is: " + str(i))

		# Don't interact with black listed users
		if usernameOfPhoto in blackListedUsers:
			utils.logMessage("User: " + usernameOfPhoto + " is blacklisted")
			continue

		shouldLike = shouldlikePhoto(photoContainer)
		shouldComment = shouldCommentOnPhoto(shouldLike, usernameOfPhoto, commentUsers)
		shouldArchive = shouldArchiveThePhoto(photoContainer, usernameOfPhoto, archiveUsers)

		if shouldLike:
			#likeButtons[i].click()
			utils.logMessage("Liked photo of user: " + usernameOfPhoto)
		if shouldComment:
			sampleComment = random.choice(sampleComments)
			postComment(driver, photoContainer, sampleComment, i)
			utils.logMessage("Commented on user '" + usernameOfPhoto + "'' with the comment '" + sampleComment + "'")
		if shouldArchive:
			#archiveButtons[i].click()
			utils.logMessage("Saved photo of user: " + usernameOfPhoto)

		interactionCount = interactionCount + 1
		utils.logMessage("Interaction Count: " + str(interactionCount + interactionsTillNow))

	return interactionCount

# Driver function for interactWithPhotos() (See README for understanding this)
def runBot(webPageData, driver):

	# Each image is wrapped with <article> (Get its class)
	articleClassName = parser.findArticleClassName(webPageData)
	articleClassSelector = parser.concatenate1(articleClassName)

	'''
		For achieving the scrolling effect (so that new images
		get loaded), we need to run javascript with the help of
		selenium

	'''

	scrollJSScript = "var elem = document.getElementsByClassName('" + articleClassName + "')[0];" + \
						"console.log(elem.scrollHeight); window.scrollBy(0, elem.scrollHeight);"

	# Get the users whom you don't want to interact with
	blackListedUsers = []
	blackListFileExists = os.path.isfile(CONSTANTS.BLACK_LIST_FILE)
	if blackListFileExists:
		blackListedUsers = utils.getDataFromFile(CONSTANTS.BLACK_LIST_FILE)

	# Get the users on whom you want to comment (and the data to comment)
	commentUsers = []
	sampleComments = []
	commentListFileExists = os.path.isfile(CONSTANTS.COMMENT_LIST_FILE)
	randomCommentListFileExists = os.path.isfile(CONSTANTS.COMMENTS_FILE)
	if commentListFileExists and randomCommentListFileExists:
		commentUsers = utils.getDataFromFile(CONSTANTS.COMMENT_LIST_FILE)
		sampleComments = utils.getDataFromFile(CONSTANTS.COMMENTS_FILE)

	archiveUsers = []
	archiveListFileExists = os.path.isfile(CONSTANTS.ARCHIVE_LIST_FILE)
	if archiveListFileExists:
		archiveUsers = utils.getDataFromFile(CONSTANTS.ARCHIVE_LIST_FILE)

	# At max, interacts with top k photos (where k = CONSTANTS.MAX_INTERACTIONS)
	totalInteractionCount = 0

	# Scroll only 100 times at max
	for iterations in range(0,100):

		interactionCount = interactWithPhotos(driver, articleClassSelector, \
										totalInteractionCount, blackListedUsers, \
										commentUsers, sampleComments, \
										archiveUsers)
		totalInteractionCount = totalInteractionCount + interactionCount
		if totalInteractionCount == CONSTANTS.MAX_INTERACTIONS:
			break
		else:
			# Scroll the page to get new photos
			driver.execute_script(scrollJSScript)
			# Wait for the page to load
			time.sleep(5 * CONSTANTS.WAIT_TIME)



