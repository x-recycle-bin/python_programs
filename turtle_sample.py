import turtle
import time

t = turtle

i = 30
flag = False

while True:
	t.forward(80)
	if flag:
		t.left(i)
		flag = False
	else:
		t.right(i)
		flag = True
	i = (i + 30) % 360



time.sleep(5) 