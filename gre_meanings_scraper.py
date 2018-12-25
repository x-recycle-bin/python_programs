
'''

	NOTE: Use this at your own disclosure.

	I do not bear anything.


'''

import requests
from bs4 import BeautifulSoup as webcrawl

def getData(meaning):
	url = "https://wordsinasentence.com/" + meaning + "-in-a-sentence/"
	print("Making a request to the URL: " + url)

	return_val = u''

	try:
		# Put some headers
		headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
		data = requests.get(url, headers=headers)
		soup = webcrawl(data.text, "html.parser")
		content = soup.find("div", {"class": "thecontent clearfix"})

		list_of_p = content.find_all("p")
		for p_tag in list_of_p:
			# print(p_tag)
			# print("\n\n\n")
			if len(p_tag.contents) > 0:
				unicode_string = p_tag.find(text=True, recursive=False)
				if unicode_string is None:
					continue
				else:
					# print("Unicode string is: " + unicode_string)
					if "vocabulary videos" not in unicode_string and "YouTube channel" not in unicode_string:
						return_val += unicode_string + u"\n"

		return return_val

	except Exception as e:
		print("Exception raised in getData(" + meaning + ") method: " + str(e))
		return return_val

def getWordList():
	with open('word_list.txt', 'r') as f:
		content = f.readlines()
	content = [x.strip() for x in content] 
	return content



# Main function

input_words = getWordList()

for word in input_words:
	
	print("\nParsing meanings for: " + word)
	
	data = ""
	try:
		data = getData(word)
	except Exception as e:
		print("Exception occurred in main method: " + str(e))
		data = word + "\nParsing error\n\n"

	with open('words_in_sentence.txt', 'a') as the_file:
	    the_file.write(data.encode('utf8'))
	    the_file.write("\n")









