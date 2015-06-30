#!/usr/bin/python

from doorway.doorway import Doorway
from time import sleep
from PIL import Image
import Queue

sacred = Doorway()
sacred.bow()

sleep(1)

#img = Image.open("doorway/res/flames.jpeg")
#img = img.resize((29, 2048))

#img = Image.open("doorway/res/rainbow.jpg")
#img = img.resize((29, 2048))


#img = Image.open("doorway/res/wedding1.jpg")
#img = img.resize((29, 960))

img = Image.open("doorway/res/water2.jpg")
img = img.resize((29, 333))

"""
img = Image.open("doorway/res/metatron.jpg")
img = img.resize((29, 1080))
"""

pixels = img.load()

for y in range(img.size[1]):
	xs = []
	for x in range(img.size[0]):
		xs.append(pixels[x, y])

	lines.append(xs)

#queue = Queue.Queue(7)
for line in lines:
	count = 0
	for sp in sacred.sheets[1]:
		sacred.pixels[sp[0]] = line[count]
		sacred.pixels[sp[1]] = line[count]
		count += 1	
	sacred.bow()

	count = 0
	for sp in (sacred.sheets[2]):
		sacred.pixels[sp[0]] = line[count]
		sacred.pixels[sp[1]] = line[count]
		count += 1	
	sacred.bow()

	count = 0
	for sp in sacred.sheets[3]:
		sacred.pixels[sp[0]] = line[count]
		sacred.pixels[sp[1]] = line[count]
		count += 1	
	sacred.bow()

	count = 0
	for sp in sacred.sheets[4]:
		sacred.pixels[sp[0]] = line[count]
		sacred.pixels[sp[1]] = line[count]
		count += 1	
	sacred.bow()

	count = 0
	for sp in sacred.sheets[5]:
		sacred.pixels[sp[0]] = line[count]
		sacred.pixels[sp[1]] = line[count]
		count += 1	
	sacred.bow()

	count = 0
	for sp in sacred.sheets[6]:
		sacred.pixels[sp[0]] = line[count]
		sacred.pixels[sp[1]] = line[count]
		count += 1	
	sacred.bow()

	count = 0
	for sp in sacred.sheets[7]:
		sacred.pixels[sp[0]] = line[count]
		sacred.pixels[sp[1]] = line[count]
		count += 1	

	sacred.bow()
	sleep(0.01)
