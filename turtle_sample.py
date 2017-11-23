import turtle
import time
import random

t = turtle

size = 10
disp = 10
i = 0

while True:
	t.forward(disp)
	t.left(60)
	if i == 2:
		disp += 10
	i = (i + 1) % 3