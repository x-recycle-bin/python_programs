import requests
from bs4 import BeautifulSoup as webcrawl
import selenium.webdriver as webdriver
import time
import re

def getStaus(name):
	url = "https://www.quora.com/profile/" + name
	print(url)

	try:
		# Put appropriate headers here later
		headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
		data = requests.get(url, headers=headers)

		soup = webcrawl(data.text, "html.parser")

		statusTag = soup.find("span", class_="IdentityCredential UserCredential")

		if hasattr(statusTag, "contents"):
			return statusTag.contents[0]
		else:
			return "No status found"

	except Exception as e:
		print(e)
		print('Extra info:' + '\nURL: ' + url)

def storeStringInFile(string, fileName, mode):
	file = open(fileName, mode)
	file.write(string)
	file.close()

# This function finds the login button on the webpage
def goToLoginPage(webPageData, driver):
	abc = re.search("Have an account?", webPageData)
	offset = abc.end(0)
	newString = webPageData[offset:offset + 40]
	classString = re.search('class="', newString)
	offset = classString.end(0)
	lastString = newString[offset:offset + 20]

	className = ""
	for char in lastString:
		if char == '"':
			break
		className = className + char

	driver.find_element_by_class_name(className).click()

# This function finds the submit button className on the webpage
def findSubmitButtonClass(webPageData, driver):
	abc = re.search("password", webPageData)
	offset = abc.end(0)
	newString = webPageData[offset:offset + 400]
	classString = re.search('button class="', newString)
	offset = classString.end(0)
	lastString = newString[offset:offset + 80]
	className = ""
	for char in lastString:
		if char == '"':
			break
		className = className + char

	mylist = className.split(" ")
	finalClassName = ""
	for item in mylist:
		finalClassName = finalClassName + "." + item

	return finalClassName

# This function finds the article-className on the webpage
def findArticleClassName(webPageData, driver):
	abc = re.search('article class="', webPageData)
	offset = abc.end(0)
	newString = webPageData[offset:offset + 50]
	className = ""
	for char in newString:
		if char == '"':
			break
		className = className + char

	return className

def getListOfPhotos():
	
	# Go to the instagram page
	url = "https://www.instagram.com/"
	driver = webdriver.Chrome()
	driver.get(url)
	# Wait for the page to load
	time.sleep(10)
	webPageData = webcrawl(driver.page_source, "html.parser").prettify()

	# Click on the login button to get the login page
	# By default we'll go to sign-up page
	goToLoginPage(webPageData, driver)
	time.sleep(10)
	# New webpage data
	webPageData = webcrawl(driver.page_source, "html.parser").prettify()

	# File username and password
	username = driver.find_element_by_name("username")
	password = driver.find_element_by_name("password")
	username.send_keys("aditya_ch_")
	password.send_keys("<>fulltp!</>")

	# Login
	submitClassName = findSubmitButtonClass(webPageData, driver)
	driver.find_element_by_css_selector(submitClassName).submit()
	time.sleep(10)
	# New web page data
	webPageData = webcrawl(driver.page_source, "html.parser").prettify()

	articleClassName = findArticleClassName(webPageData, driver)
	print(articleClassName)
	
	# script = "function scrollingFunction() {var elem = document.getElementsByClassName('_s5vjd _622au _fsupd _8n9ix')[0]; console.log(elem); window.scrollTo(0, elem.scrollHeight); } scrollingFunction();"
	script = "console.log('Executing script in driver'); var elem = document.getElementsByClassName('" + articleClassName + "')[0]; console.log(elem); window.scrollBy(0, elem.scrollHeight);console.log('Scrolling by height: ' + elem.scrollHeight)"
	print(script)

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
	storeStringInFile(dataToWrite, "insta_temp.html", "a")
	#print("Writing to file")
	#writeStringToFile(webcrawl(driver.page_source, "html.parser").prettify(), "insta_temp.html")
	#print("Written")

	#soup = webcrawl(driver.page_source, "html.parser")
	#dump = soup.prettify()'''


if __name__ == "__main__":
	getListOfPhotos()