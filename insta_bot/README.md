# Insta-Bot
An Instagram-Bot which has the ability to interact with a given instagram feed. This project was developed to demonstrate my python programming skills. To be more specific: Web-scraping in python and using basic external modules such as Selenium.

<img src="./insta-bot-img.jpeg" width="300" height="200" />

<h2>Features</h2>
<ul>
  <li>Auto-Likes photos</li>
  <li>Auto-Saves photos within instagram</li>
  <li>Ability to black-list users</li>
  <li>Watch stories</li>
</ul>

<h2>Running the Project</h2>
This project is written entirely in python3. Download <a href="https://www.python.org/downloads/">python</a>, along with the following modules:
<ul>
  <li><a href="https://pypi.python.org/pypi/beautifulsoup4">BeautifulSoup python module</a></li>
  <li><a href="https://pypi.python.org/pypi/selenium">Selenium python module</a></li>
  <li><a href="https://sites.google.com/a/chromium.org/chromedriver/downloads">Selenium Chrome Driver</a>. After downloading this, store it in /usr/local/bin/ directory</li>
  <li>Regular Expression python module (Usually comes in-built)</li>
</ul>
There are several ways you can install the python modules, including but not limited to: <b>pip</b>, <b>easy_install</b>, etc.

Once the setup is done, run the following command on the terminal:<br>
<br><code>python3 start.py /absolute/path/to/credentials/file.txt</code><br><br>
The bot expects you to store the credentials in a file on your desktop, and supplied to it on the command line. The format of the credentials file is as follows:<br>
<ul>
  <li><i>username-of-your-instagram-account</i> (on first line)</li>
  <li><i>password-of-your-instagram-account</i> (on second line)</li>
</ul>

After running the above command, simultaneously open <i>'logs.txt'</i> file in the same directory as the project to see what the bot is doing. Alternatively, you can open another terminal and navigate to this project directory and run the command:<br>
<br><code>tail -f ./logs.txt</code><br><br>

Congrats, your own personal bot is up and running! If you find any problem deploying the project in your machine, please do let me know.

Note: This project is tested on Chrome browser (which opens in an headless state). The python version used is python 3.6.1 on MacOS High Sierra.<br>

<h2>Using the bot</h2><br>
By default, the insta-bot does only the like operation on photos present in your instagram feed. If you want to make the bot use other features too, then:
<ul>
  <li><b>Using Auto-Save feature:</b> Instagram provides an option to save (within instagram itself) on every photo present in your feed. By default the bot doesn't save the photo. You have to tell it explicitly. Create a file named <i>'archiveUsers.txt'</i> which contains the instagram usernames of the users whose photos you would love to save. All the usernames must be on new line. If you run the bot now, the bot will obey you and save the photos of the users whom you have specified (only if it finds the photos of those users in the feed).</li>
  <li><b>Black listing users:</b> There will be some situations when you don't want the bot to like all the photos which appear on your instagram feed. You want to exclude few users., i.e. you want to black-list few users. You can inform this to the bot by creating another file named <i>'blackList.txt'</i> which follows the same format as <i>'archiveUsers.txt'</i>.</li>
  <li><b>Watch Instagram Stories:</b> The bot can watch instagram-stories on behalf of you. To do this you half to make a few changed in the source code. Specifically in the start.py file. Open the file and read-through the comments to understand what to do. (Basically you need to comment and uncomment few lines to start the browser in normal-state. Reason being, you cannot watch the stories when your browser runs in headless state)</li>
  <li><b>Schedule the bot:</b> Running the bot manually by typing in the command on a terminal is not interesting. To make it fully autonomous, run the above command as a cronjob (by making it a background-repetitive-task). You can always monitor what the bot is doing by looking into <i>'logs.txt'</i></li>
</ul><br>

<h2>Mechanics of the bot</h2><br>

At the time of writing this, instagram home-page structure is as follows:
Each post which we see in the instagram feed, has an actual-photo and like-button among other things.
We exploit this DOM (Document Object Model) structure here to access the like-button and perform our operation. We use the <i>BeautifulSoup</i> python module to perform this web scraping.<br><br>
We use <i>Selenium</i> module to perform the actual like and save operations<br><br>
Instagram loads the images in a bizzare manner. First call to load the home-page (i.e. instagram feed) will load only few (i.e. 4 or 5) images. As we scroll down, it adds new images to the feed. After a certain count (say 7 or 8 images), when the next image will be loaded, it will be placed on the top (i.e. first image content will be overwritten with this new image content). This process might be efficient for instagram, but it makes our bot-programming a bit tedious.<br>

<h2>Development</h2><br>
<ul>
  <li>Sublimt Text has been used to code the entire project</li>
  <li>Chrome browser in headless state. If you prefer to use another browser, then download the corresponding driver for selenium and make appropriate changes in the source code</li>
  <li>Almost every file is descriptive in nature. Comments provide in-depth explanation about what's going on. Do have a look at the code. It's well crafted</li>
</ul><br>

<h2>TO DO</h2><br>
<ul>
  <li><b>Comment feature:</b> Bot will be able to comment on your behalf. The comment will be chosen from a random list of sample comments provided by the user in a file</li>
  <li><b>User Interface: </b> Currently the bot operates on a CLI. Everything looks good with UI!</li>
</ul>

Use this, report bugs, raise issues and Have fun. Do whatever you want! I would love to hear your feedback :)

~ Happy Coding
