'''
	
	Python program which gives you a list of questions
	to answer on Quora, based on followers and number of
	existing answers

'''

from bs4 import BeautifulSoup as webcrawl
import random

def parseQuoraQuestionFeed(filename):

	# Read the HTML file
	content = ""
	with open(filename, "r") as f:
		content = f.read()

	'''
		Start parsing the document for required entities:
		
		We require the following:

		(i) Question Name
		(ii) Existing Answers
		(iii) Number of followers

		Note: This is a hardcoded version of HTML class attributes and
		we need to change this to something concrete to make it error-prone
		so that the code doesn't break if Quora changes its UI or HTML
		skeleton. For instance, if Quora provides an API to access
		topic-question-feed then we do not need to follow this approach

	'''

	soup = webcrawl(content, "html.parser")

	questionList = soup.findAll("div", {"class": "QuestionFeedStory FeedStory feed_item"})

	results = []
	for question in questionList:
		
		questionName = question.find('span', class_="ui_qtext_rendered_qtext")
		
		existingNumAnswers = question.find('a', class_="answer_count_prominent")
		if existingNumAnswers.text == "No answer yet":
			existingNumAnswers = 0
		else:
			existingNumAnswers = int(existingNumAnswers.text.split()[0])

		followButton = question.find('div', class_="ItemComponent FollowActionItem primary_item")
		if followButton == None:
			followButton = question.find('div', class_="FollowActionItem ItemComponent primary_item")
		
		followCountWrapper = followButton.find('span', class_="icon_action_bar-count")
		followerCount = followCountWrapper.find_all('span')[1].text

		# Prepare a dictionary and keep appending to the list

		result = {
			"questionName": questionName.text,
			"existingAnswers": existingNumAnswers,
			"followers": followerCount
		}

		results.append(result)

	return results

def merge(l1, l2):
	'''
		Currently, these 2 lists are merely concatenated but there
		are other alternatives such as:

		(i) Randomly mix the 2 lists so that you won't be answering
		only "Top" questions but you will also be writing answers to
		"Popular" questions

		(ii) Add weight to the lists using some threshold value so
		that we get more fine-grained recommendations. What I mean
		by this is, we should add another attribute to the "top"
		questions list such as "Last followed" so that we can give
		additional priority to it

	'''
	return l1 + l2

def getRecommendedQuestions(results, desiredFollowerCount):

	recommendedQuestions = []
	topQuestions = []
	popularQuestions = []

	i = 0
	for i in range(0, len(results)):
		
		question = results[i]

		'''
			Currently the questions are classified into 2 categories:

			(i) Top questions: those which have a higher followers-to-existingAnswers
			ratio

			(ii) Popular questions: those which have no existing answers but have
			too many followers

		'''

		if question["existingAnswers"] != 0:
			factor = int(question["followers"]) / int(question["existingAnswers"])
			topQuestions.append({"factor": factor, "index": i})
		elif int(question["followers"]) > desiredFollowerCount:
			popularQuestions.append({"factor": None, "index": i})

	topQuestions = sorted(topQuestions, key=lambda k: k['factor'], reverse=True) 

	questionsToAnswer = merge(topQuestions, popularQuestions)

	# After finding the 2 categories of questions mix them up and append to the final list
	for question in questionsToAnswer:
		recommendedQuestions.append(results[question["index"]]["questionName"])

	return recommendedQuestions

if __name__ == "__main__":

	# File which contains the HTML content
	filename = "/Users/adityach/Desktop/abc.html"
	desiredFollowerCount = 100

	results = parseQuoraQuestionFeed(filename)
	print(results)
	recommendedQuestions = getRecommendedQuestions(results, desiredFollowerCount)
	print("You can answer the following questions: \n")
	print(recommendedQuestions)








