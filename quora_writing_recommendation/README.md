
# A crawler which recommends what questions to answer

I frequently write on Quora, and oftentimes I find that it becomes increasingly harder to find a question which is either popular or "in demand" (I would like to call it a 'top' question) whenever I visit a topic's top questions page. For instance:

  https://www.quora.com/topic/Marvel-Cinematic-Universe/top_questions

the above link is a top-questions webpage of Quora, for the topic: "Marvel Cinematic Universe" (One of my favorite topics)

Nevertheless, Quora does an excellent job from its side by ensuring that whenever a user visits such a webpage, irrespective of the topic, the algorithms come into play which unsurprisingly uses some sophisticated mechanisms to relatively measure a questions importance to the user.

But from a users perspective, at least from my perspective I sometimes (bear in mind, not all the times! :D) prefer to answer questions which fall into one of the two categories:

<ul>
  <li><b>Top questions</b> - those which have a <i>higher-number-of-followers</i> to <i>existing-answers</i> ratio. If you were to answer such a question, then by definition, your answer will reach more number of people. I would like to call this an objective metric. In other words, it does not vary from user to user.</li>
  <li><b>Popular questions</b> - those which have no existing answers but have too many followers. This metric is subjecive and hence specific to each individual user. 100 followers might be too many for a particular question for some users, whereas 1K followers to a particular question does not even seem to be in the ballpark for Quora Top Writers, for example.</li>
</ul>

I was in a verbose mode while developing this program and consequently the working of the program is heavily documented within <i>crawl.py</i> itself.

<h2>Using the crawler</h2>
This project is written entirely in python3 (Note: Since there is some basic math involved in the crawler the division operator '/' might not work as expected in Python2 when compared to Python3). Download <a href="https://www.python.org/downloads/">python3</a>, along with the <a href="https://pypi.python.org/pypi/beautifulsoup4">BeautifulSoup</a> python module for web scraping <br/><br/>

There are several ways you can install the python modules, including but not limited to: <b>pip</b>, <b>easy_install</b>, etc.

After installation, you need to edit few variables within the file. As mentioned previously, set <i>desiredFollowerCount</i> as per your requirement and copy the HTML content from any one of the topic's top-questions webpage from Quora into a particular file into your local system. You can use the above mentioned link to copy the HTML content of "Marvel Cinematic Universe" topic from Quora for getting started.

Finally, change the <i>filename</i> variable in the script to point to the file in which you have saved the HTML content. Run the following command on the terminal:<br>
<br><code>python3 crawl.py </code><br><br>

The crawler dumps a list of recommended questions for you, onto the console! Enjoy Writing :)

If you find any problem deploying the project in your machine, please do let me know.

Note: The python version used to develop this script is python 3.6.1 on MacOS High Sierra.<br>

<h2>TO DO</h2><br>
<ul>
  <li><b>Use Quora's API: </b> Currently, as far as I have tested on various topics, the crawler works flawlessly, nonetheless it is highly tied to the current implementation of Quora's website and therefore can break at any time. </li>
  <li><b>Final automation: </b> To put it in a nutshell, the HTTP module is missing to make the crawler fully automated. Once this is done, you will simply feed in a URL (or even a topic name) to the program and it does the rest of the job for you</li>
  <li><b>Integrate it to Chrome as an extension: </b> This way you will not be required to run any kind of a script on your local machine</li>
</ul>

Use this, report bugs, raise issues and Have fun. Do whatever you want! I would love to hear your feedback :)

~ Happy Coding
