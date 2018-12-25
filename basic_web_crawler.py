'''

	NOTE: Use this at your own disclosure.

	I do not bear anything.


'''

import requests
from bs4 import BeautifulSoup as webcrawl


def getStaus(name):
    url = "https://www.quora.com/profile/" + name
    print(url)

    try:
        # Put appropriate headers here later
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        data = requests.get(url, headers=headers)

        soup = webcrawl(data.text, "html.parser")

        statusTag = soup.find("span", \
                              class_="IdentityCredential UserCredential")

        if hasattr(statusTag, "contents"):
            return statusTag.contents[0]
        else:
            return "No status found"

    except Exception as e:
        print(e)
        print('Extra info:' + '\nURL: ' + url)


def makeRequest(name):
    status = getStaus(name)
    dataToFile = name + ': ' + status + '\n'
    file = open("quora_statuses.txt", "a")
    file.write(dataToFile)
    file.close()


with open("list_of_names.txt", "r") as f:
    for line in f:
        aLine = line.split()
        if len(aLine) >= 2:
            name = aLine[0] + '-' + aLine[1]
            makeRequest(name)
            for i in range(1, 10):
                makeRequest(name + '-' + str(i))
