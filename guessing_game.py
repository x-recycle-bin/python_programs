import random

try:

	n = random.randint(0, 100)
	while True:
		num = input('Enter a number: ')
		if num == n:
			print('Success!')
			break
		elif num < n:
			print('You underestimated the number. Try again.')
		else:
			print('You overestimated the number. Try again.')

except:

	print('Input error occurred')