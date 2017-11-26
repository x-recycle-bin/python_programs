'''
	@file: parser.py

	@desc: Contains functions which parse input data

'''
import re

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
	Input is a space separated strings
	and output is a string
	which is formed by concatenating
	all the strings with '.'

'''
def concatenate1(string):

	mylist = string.split(" ")
	returnString = ""
	for item in mylist:
		returnString = returnString + "." + item

	return returnString

'''
	Input is a string, in the form:

	"['abc', 'def', 'ghi', ...]"

	Output is a string in the form:

	".abc.def.ghi"

'''
def concatenate2(string):

	returnString = ""
	aString = ""
	started = False

	for i in range(0, len(string)):
		
		char = string[i]

		if char == "'":
			if started == False:
				started = True
			else:
				started = False
				returnString = returnString + "." + aString
				aString = ""
		elif started:
			aString = aString + char

	return returnString

'''
	Given an input string, this function finds
	the first occurence of the substring and
	returns the position where the substring
	ends in the main string

'''
def findOffsetAfter(substring, string):

	result = re.search(substring, string)
	return result.end(0)

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