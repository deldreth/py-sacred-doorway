#!/usr/bin/python

from doorway.doorway import *
from time import sleep
from colors import ColorWheel
from Queue import Queue

# sacred  = Doorway()
sacred = Doorway(client="192.168.1.142:7890")

def wheel(value):
	if value < 85:
		return (value * 3, 255 - value * 3, 0)
	elif value < 170:
		value -= 85
		return (255 - value * 3, 0, value * 3)
	else:
		value -= 170
		return (0, value * 3, 255 - value * 3)

q1 = Queue()

t1 = DoorwayAnimations(q1)
t1.animations.put({'sheets' : (1, 2), 'rgb' : (255, 0, 0), 'sleep' : 0.01})
t1.animations.put({'sheets' : (3, 4), 'rgb' : (0, 255, 0), 'sleep' : 0.01, 'direction' : 'up'})
t1.animations.put({'sheets' : (5, 6), 'rgb' : (0, 0, 255), 'sleep' : 0.01})
t1.start()
t1.join()

t1 = DoorwayAnimations(q1)
t1.animations.put({'sheets' : (1, 2, 3, 4, 5, 6, 7), 'rgb' : (0, 0, 0), 'sleep' : 0})
for x in range(256):
	t1.animations.put({'sheets' : (1, 3, 5, 7), 'rgb' : wheel(x), 'sleep' : 0})
	# t2.animations.put({'sheets' : (2, 4, 6), 'rgb' : wheel(x+50), 'sleep' : 0})

t1.start()
t1.join()

sacred.put(2, rgb = (255, 255, 255))
sacred.put(4, rgb = (255, 255, 255))
sacred.put(6, rgb = (255, 255, 255))
sacred.bow()

# for y in range(100):
# 	for x in range(256):
# 		sacred.put(1, rgb = wheel(x))
# 		sacred.put(2, rgb = wheel(x+10))
# 		sacred.put(3, rgb = wheel(x+20))
# 		sacred.put(4, rgb = wheel(x+30))
# 		sacred.put(5, rgb = wheel(x+20))
# 		sacred.put(6, rgb = wheel(x+10))
# 		sacred.put(7, rgb = wheel(x))
# 		sacred.bow(0.1)

# for sheet in sacred.sheets:
# 	for l, r in sacred.sheets[sheet]:
# 		sacred.pixels[l] = (255, 0, 0)
# 		sacred.pixels[r] = (255, 0, 0)

# 		sacred.bow(0.01)

# 	for l, r in reversed(list(sacred.sheets[sheet])):
# 		sacred.pixels[l] = (0, 255, 0)
# 		sacred.pixels[r] = (0, 255, 0)

# 		sacred.bow(0.01)