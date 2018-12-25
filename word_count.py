import sys

# counts words from a file
# specify the filename as a command line argument

if len(sys.argv) != 2:
	print("\nError! Usage: python word_count.py <filename>\n")
	exit(1)

filename = sys.argv[1]
words = 0

with open(filename,'r') as f:
    for line in f:
        for word in line.split():
        	print(word)
        	words = words + 1

print("\nWord count: " + str(words) + "\n")