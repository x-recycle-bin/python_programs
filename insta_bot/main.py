import requests
from bs4 import BeautifulSoup as webcrawl
import selenium.webdriver as webdriver
import time
import re
import sys

WAIT_TIME = 3
MAX_PHOTO_LIKES = 10

def storeStringInFile(string, fileName, mode):
	file = open(fileName, mode)
	file.write(string)
	file.close()

'''
	Given an input string, this function finds
	the first occurence of the substring and
	returns the position where the substring
	ends in the main string

'''
def findOffsetAfter(substring, string):

	result = re.search(substring, string)
	return result.end(0)

'''
	Parses subtring from an input string which
	is in the format:

	string = 'abcdefg...." <span> ... etc'

	And returns:

	'abcdefgh....'

'''
def parseClassName(string):

	className = ""
	for char in string:
		if char == '"':
			break
		className = className + char

	return className

'''
	Input is a space separated list
	of strings and output is a string
	which is formed by concatenating
	all the strings with '.'

'''
def concatenate(string):

	mylist = string.split(" ")
	returnString = ""
	for item in mylist:
		returnString = returnString + "." + item

	return returnString

# Finds the login button on signup-page and returns its class
def findLoginButton(webPageData):

	offset1 = findOffsetAfter("Have an account?", webPageData)
	loginString = webPageData[offset1:offset1 + 40]

	offset2 = findOffsetAfter('class="', loginString)
	classNameString = loginString[offset2:offset2 + 20]

	return parseClassName(classNameString)

# Finds the submit button on login-page and returns its class
def findSubmitButton(webPageData):

	offset1 = findOffsetAfter("password", webPageData)
	submitString = webPageData[offset1:offset1 + 400]

	offset2 = findOffsetAfter('button class="', submitString)
	classNameString = submitString[offset2:offset2 + 80]

	return parseClassName(classNameString)

# Finds the article-className on homePage and returns it
def findArticleClassName(webPageData):

	offset1 = findOffsetAfter('article class="', webPageData)
	articleClassString = webPageData[offset1:offset1 + 50]

	return parseClassName(articleClassString)

def getListOfPhotos():
	pass	


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
	This function loads the login page and returns it
	in the form of a string

'''
def openLoginPage(driver, url):

	# By default we go to the sign-up page
	driver.get(url)
	# Wait for the page to load
	time.sleep(WAIT_TIME)

	'''
		On the sign-up page we need to
		find the login button and click
		it, so that we go to login page

	'''
	signUpPageSrc = driver.page_source
	signUpPageData = str(webcrawl(signUpPageSrc, "html.parser"))

	loginButton = findLoginButton(signUpPageData)
	driver.find_element_by_class_name(loginButton).click()
	# Wait for the page to load
	time.sleep(WAIT_TIME)

	loginPageSrc = driver.page_source
	loginPageData = str(webcrawl(loginPageSrc, "html.parser"))

	return loginPageData

# Likes a photo on the given page
def likePhoto(webPageData, driver, photosLiked):
	pass # TODO

# Driver function for likePhoto (See README for understanding this)
def runBot(webPageData, driver):

	# Each image is wrapped with <article> (Get its class)
	articleClassName = findArticleClassName(webPageData)

	'''
		For achieving the scrolling effect (so that new images
		get loaded), we need to run javascript with the help of
		selenium
	'''

	scrollJSScript = "var elem = document.getElementsByClassName('" + articleClassName + "')[0];" + \
						"window.scrollBy(0, elem.scrollHeight);"

	# At max, likes top 10 unliked-photos
	photosLiked = 0
	while True:
		likeCount = likePhoto(webPageData, driver, photosLiked)
		photosLiked = photosLiked + likeCount
		if photosLiked == MAX_PHOTO_LIKES:
			break
		else:
			# Scroll the page to get new photos
			driver.execute_script(scrollJSScript)
			# Wait for the page to load
			time.sleep(3 * WAIT_TIME)
			# Update webPageData
			webPageData = str(webcrawl(driver.page_source, "html.parser"))

	'''
	waitTime = 3 # in seconds

	# Single iteration (likes must be performed here itself by checking the status of the like button)
	time.sleep(waitTime)
	dataToWrite = str(webcrawl(driver.page_source, "html.parser").find_all("div", class_="_eeohz")) + "\n"
	storeStringInFile(dataToWrite, "insta_temp.html", "w")
	time.sleep(waitTime)
	driver.execute_script(script)

	time.sleep(waitTime)
	dataToWrite = str(webcrawl(driver.page_source, "html.parser").find_all("div", class_="_eeohz")) + "\n"
	storeStringInFile(dataToWrite, "insta_temp.html", "a")
	driver.execute_script(script)

	time.sleep(waitTime)
	dataToWrite = str(webcrawl(driver.page_source, "html.parser").find_all("div", class_="_eeohz")) + "\n"
	storeStringInFile(dataToWrite, "insta_temp.html", "a")
	driver.execute_script(script)

	time.sleep(waitTime)
	dataToWrite = str(webcrawl(driver.page_source, "html.parser").find_all("div", class_="_eeohz")) + "\n"
	storeStringInFile(dataToWrite, "insta_temp.html", "a")'''

def login(url, driver):

	credentials = getCredentials(sys.argv[1])

	loginPageData = openLoginPage(driver, url)

	# Find the submit button on login page
	submitClassName = findSubmitButton(loginPageData)
	submitClassName = concatenate(submitClassName)

	# Find username and password
	username = driver.find_element_by_name("username")
	password = driver.find_element_by_name("password")
	username.send_keys(credentials["username"])
	password.send_keys(credentials["password"])

	# Do the login
	driver.find_element_by_css_selector(submitClassName).submit()
	# Wait for the page to load
	time.sleep(3 * WAIT_TIME)

	homePageSrc = driver.page_source
	homePageData = str(webcrawl(homePageSrc, "html.parser"))

	return homePageData

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
	homePageData = login(url, driver)

	# Like photos
	runBot(homePageData, driver)

'''
	Invoke this program as:

	$ python main.py /absolute/path/to/credentials/file.txt

	The credentials file must contain your instagram
	username on first-line and password on second-line

	It must be a text file

'''

if __name__ == "__main__":

	try:
	
		if len(sys.argv) != 2:
			print("Error (Missing arguments): Usage is\npython main.py /absolute/path/to/credentials/file.txt")
			quit()

		main()

	except Exception as e:
		print(e)
