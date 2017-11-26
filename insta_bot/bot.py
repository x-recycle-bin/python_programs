'''
	@file: bot.py

	@desc: Contains functions specific to running the bot

'''

import time
import re
import os.path
from bs4 import BeautifulSoup as webcrawl
import constants as CONSTANTS
import parser
import utils

def getBlackListedUsers():

	with open(CONSTANTS.BLACK_LIST_FILE) as f:
		content = f.readlines()

	# remove whitespace characters like `\n` at the end of each line
	content = [x.strip() for x in content]
	return content

# Likes photos on the given page
def likePhotos(driver, articleClassSelector, photosLikedTillNow, blackListedUsers):

	likeCount = 0

	# Find all photos in the current page
	photolist = driver.find_elements_by_css_selector(articleClassSelector)

	# Find all like button links corresponding to these photos
	likeButtonClass = str(webcrawl(photolist[0].get_attribute('innerHTML'), "html.parser").contents[2].contents[0].find("a").attrs["class"])
	likeButtonClassSelector = parser.concatenate2(likeButtonClass)
	likeButtons = driver.find_elements_by_css_selector(likeButtonClassSelector)

	for i in range(0, len(photolist)):

		# Find the username to which the photo belongs
		photoContainer = photolist[i].get_attribute('innerHTML')
		usernameOfPhoto = str(webcrawl(photoContainer, "html.parser").header.contents[1].contents[0].contents[0].contents[0].contents[0])

		# Don't interact with black listed users
		if usernameOfPhoto in blackListedUsers:
			utils.logMessage("User: " + usernameOfPhoto + " is blacklisted")
			continue

		# Find whether we have already liked the photo or not
		likeStatusContent = str(webcrawl(photoContainer, "html.parser").contents[2].contents[0].contents[0])
		if bool(re.search(CONSTANTS.WHITE_LIKE_BUTTON_CLASS, likeStatusContent)):
			liked = False
		else:
			liked = True

		# Like the photo, if not liked previously
		if liked == False:

			if (photosLikedTillNow + likeCount) == CONSTANTS.MAX_PHOTO_LIKES:
				break
			else:
				# likeButtons[i].click()
				likeCount = likeCount + 1
				utils.logOperation(usernameOfPhoto, likeCount + photosLikedTillNow)

	return likeCount

# Driver function for likePhoto (See README for understanding this)
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
						"window.scrollBy(0, elem.scrollHeight);"

	# Get the users whom you don't want to interact with
	blackListedUsers = []
	blackListFileExists = os.path.isfile(CONSTANTS.BLACK_LIST_FILE)
	if blackListFileExists:
		blackListedUsers = getBlackListedUsers()

	# At max, likes top k unliked-photos (where k = CONSTANTS.MAX_PHOTO_LIKES)
	photosLiked = 0

	# Scroll only 100 times at max
	for iterations in range(0,100):

		likeCount = likePhotos(driver, articleClassSelector, photosLiked, blackListedUsers)

		photosLiked = photosLiked + likeCount
		if photosLiked == CONSTANTS.MAX_PHOTO_LIKES:
			break
		else:
			# Scroll the page to get new photos
			driver.execute_script(scrollJSScript)
			# Wait for the page to load
			time.sleep(3 * CONSTANTS.WAIT_TIME)



