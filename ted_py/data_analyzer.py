import csv
import matplotlib.pyplot as plt
import numpy as np
import pandas
from collections import Counter

'''
	This function converts a string in the below
	format to a list

	input to this function:
	str = "['abc', 'def', 'ghi']"

	output of this function:
	list = ['abc', 'def', 'ghi']

'''
def convertToList(tag_string):

	str_list = tag_string.split("'")
	del str_list[0::2]
	return str_list

'''
	This function adds a list of tags,
	each element of which has a viewcount
	of 'aNumber' to a dictionary of
	<tag, viewcount>
'''
def addToDict(aList, aNumber, aDict):

	for tag in aList:
		added = False
		for key, value in aDict.items():
			'''
				 Check if the dictionary
				 already has an element with
				 this tag present.

				 If yes, then increment the
				 corresponding viewcount.

				 Else, add a new entry
			'''
			if key == tag:
				aDict[key] += aNumber
				added = True
				break
		if added == False:
			aDict[tag] = aNumber

# Reads a .csv file
def csv_dict_reader(file_obj):
    
    reader = csv.DictReader(file_obj, delimiter=',')
    # Holds the contents of the file in the form of dictionary
    mydict = {}

    for item in reader:

    	'''
			The dataset contains several attributes
			Take only those which are required (tags, views)
    	'''

    	tag_string = item["tags"]
    	tags = convertToList(tag_string)
    	views = item["views"]
    	
    	'''
			Here we make the following assumption:

			If a TED talk has got 6 views and has the following
			tags associated with it:
				tagA, tagB, tagC

			Then we distribute the views evenly as:
				tagA = 2 views
				tagB = 2 views
				tagC = 2 views
			(i.e. each tag has the same weightage in deterining
			the viewcount)

    	'''
    	viewCount = int(views) / len(tags)

    	# View count is in millions
    	viewCount = viewCount / 1000000

    	addToDict(tags, viewCount, mydict)

    return mydict

# Plots a histogram from a given dictionary of (string, float)
def plot_histogram(dataset):

	'''
		First, collect all x-axis values and y-axis
		values from the input dictionary.

		The x-axis contains the categories, which
		are strings. But in the plot we'll use their
		indices. i.e., instead of printing the category
		string on the plot, we'll print a number which
		indicates its index.

		You can find the category corresponding to that
		index in the results.txt file
		
	'''

	# Collect required data
	indices = []
	y_values = []
	itr = 0
	for key, value in dataset.items():
		indices.append(itr)
		itr = itr + 1
		y_values.append(value)

	# Plot the data
	plt.bar(indices, y_values, linewidth = 10.0)
	plt.xticks(indices, indices)
	plt.xlabel("Categories")
	plt.ylabel("Views (in millions)")

	# Save it!
	figure = plt.gcf()
	figure.set_size_inches(80, 3)
	plt.savefig('plot.png', dpi = 200)

# Writes a dictionary to a file
def store_dataset(dataset):
	file = open("./results.txt", "w")
	for key, value in dataset.items():
		file.write(key + "," + str(value) + "\n")
	file.close()

if __name__ == "__main__":

	# Read the dataset
    with open("./ted_main.csv") as f_obj:
        dataset = csv_dict_reader(f_obj)

    # Plot the histogram and save it to file
    plot_histogram(dataset)

    # Stores the data (used for plotting the histogram) into a file
    store_dataset(dataset)






