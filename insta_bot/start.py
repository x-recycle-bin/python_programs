'''
	@file: start.py

	@desc: A bot which likes, comments and saves
	photos on instagram!

	@author Aditya Ch (https://github.com/aditya-code-blooded)

'''

import sys
import selenium.webdriver as webdriver
import login as auth
import utils
import bot

def main():

	'''
		Currently works only for chrome browser.

		Ensure that you have chrome browser installed,
		along with chromedriver binary provided by
		selenium.

	'''

	# Go to the instagram page using Selenium
	url = "https://www.instagram.com/"

	driver = webdriver.Chrome()

	# Login to instagram
	homePageData = auth.login(url, driver)

	# Run the bot to like photos
	bot.runBot(homePageData, driver)

'''
	Invoke this program as:

	$ python start.py /absolute/path/to/credentials/file.txt

	The credentials file must contain your instagram
	username on first-line and password on second-line

	It must be a text file

'''

if __name__ == "__main__":

	errorString = ""

	try:
	
		if len(sys.argv) != 2:
			errorString = "Error (Missing arguments): Usage is\npython start.py /absolute/path/to/credentials/file.txt"
			utils.logMessage("Error occurred:\n" + errorString)
			quit()

		utils.logMessage("============== Starting Insta-bot ==============")
		main()

	except Exception as e:
		errorString = str(e)
		utils.logMessage("Error occurred:\n" + errorString)

	utils.logMessage("============== Insta-bot terminated ==============")

