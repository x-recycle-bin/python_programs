'''
	@file: start.py

	@desc: A bot which likes and saves
	photos on instagram! It also watches stories.

	@author Aditya Ch (https://github.com/aditya-code-blooded)

'''

import sys
import selenium.webdriver as webdriver
import login as auth
import utils
import bot
import os

def main():

	'''
		Currently works only for chrome browser.

		Ensure that you have chrome browser installed,
		along with chromedriver binary provided by
		selenium.

	'''

	# Go to the instagram page using Selenium
	url = "https://www.instagram.com/"

	# Start Chrome in headless state
	chrome_options = webdriver.chrome.options.Options()
	chrome_options.add_argument("--headless")
	driver = webdriver.Chrome(chrome_options=chrome_options)

	'''
		Note: You cannot watch Instagram stories when you
		open the browser in headless state.

		If you want to open chrome browser without the
		headless state and watch instagram stories, then
		comment out the above 3 lines and uncomment
		the below line:

	'''
	#river = webdriver.Chrome()

	# Login to instagram
	utils.logMessage("Bot is logging into Instagram")
	homePageData = auth.login(url, driver)
	utils.logMessage("Bot is successfully logged into Instagram")

	# Run the bot
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

