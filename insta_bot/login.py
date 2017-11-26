'''
	@file: login.py

	@desc: Contains functions which help in logging into
	instagram

'''

import time
import sys
from bs4 import BeautifulSoup as webcrawl
import constants as CONSTANTS
import parser

'''
	Reads username and password from the credentials file
	and returns them in the form of a dictionary

'''
def getCredentials(fileName):

	credentials = dict()

	with open(fileName) as credentialsFile:
		content = credentialsFile.readlines()

	# remove whitespace characters like `\n` at the end of each line
	content = [x.strip() for x in content] 
	credentials["username"] = content[0]
	credentials["password"] = content[1]

	return credentials

'''
	Loads the login page and returns it
	in the form of a string

'''
def openLoginPage(driver, url):

	# By default we go to the sign-up page
	driver.get(url)
	# Wait for the page to load
	time.sleep(CONSTANTS.WAIT_TIME)

	'''
		On the sign-up page we need to
		find the login button and click
		it, so that we go to login page

	'''
	signUpPageSrc = driver.page_source
	signUpPageData = str(webcrawl(signUpPageSrc, "html.parser"))

	loginButton = parser.findLoginButton(signUpPageData)
	driver.find_element_by_class_name(loginButton).click()
	# Wait for the page to load
	time.sleep(CONSTANTS.WAIT_TIME)

	loginPageSrc = driver.page_source
	loginPageData = str(webcrawl(loginPageSrc, "html.parser"))

	return loginPageData

def login(url, driver):

	credentials = getCredentials(sys.argv[1])

	loginPageData = openLoginPage(driver, url)

	# Find the submit button on login page
	submitClassName = parser.findSubmitButton(loginPageData)
	submitClassName = parser.concatenate1(submitClassName)

	# Find username and password
	username = driver.find_element_by_name("username")
	password = driver.find_element_by_name("password")
	username.send_keys(credentials["username"])
	password.send_keys(credentials["password"])

	# Do the login
	driver.find_element_by_css_selector(submitClassName).submit()
	# Wait for the page to load
	time.sleep(3 * CONSTANTS.WAIT_TIME)

	homePageSrc = driver.page_source
	homePageData = str(webcrawl(homePageSrc, "html.parser"))

	return homePageData


