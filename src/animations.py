#!/usr/bin/python

""" Ideally some of these could be rolled into a subclass of Doorway. DoorwayAnimations? """

from doorway.doorway import *
from time import sleep
from colors import ColorWheel

sacred  = Doorway(client="192.168.1.142:7890")

def wheel(value):
	if value < 85:
		return (value * 3, 255 - value * 3, 0)
	elif value < 170:
		value -= 85
		return (255 - value * 3, 0, value * 3)
	else:
		value -= 170
		return (0, value * 3, 255 - value * 3)

for x in range(256):
	sacred.put(1, rgb = wheel(x))
	sacred.put(2, rgb = wheel(x+10))
	sacred.put(3, rgb = wheel(x+20))
	sacred.put(4, rgb = wheel(x+30))
	sacred.put(5, rgb = wheel(x+20))
	sacred.put(6, rgb = wheel(x+10))
	sacred.put(7, rgb = wheel(x))
	sacred.bow(0.1)
	

for sheet in sacred.sheets:
	for l, r in sacred.sheets[sheet]:
		sacred.pixels[l] = (255, 0, 0)
		sacred.pixels[r] = (255, 0, 0)

		sacred.bow(0.01)

	for l, r in reversed(list(sacred.sheets[sheet])):
		sacred.pixels[l] = (0, 255, 0)
		sacred.pixels[r] = (0, 255, 0)

		sacred.bow(0.01)