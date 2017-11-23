import sys

n = int(input("Enter n: "))

# Check for input here

for i in range(2, n):
	isPrime = True
	for j in range(2, i):
		if i % j == 0:
			isPrime = False
	if isPrime:
		sys.stdout.write(str(i) + ' ')

print('')