'''
	@file: start.py

	@desc: A bot which likes photos on instagram!

	This project is developed by one-and-only
	-Aditya Ch

	https://github.com/aditya-code-blooded

'''

import sys
import selenium.webdriver as webdriver
import login as auth
import utils

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
	runBot(homePageData, driver)

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
			utils.logError(errorString)
			quit()

		main()

	except Exception as e:
		errorString = str(e)
		utils.logError(errorString)


