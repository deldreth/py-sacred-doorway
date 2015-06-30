#!/usr/bin/python

from doorway.doorway import Doorway
from time import sleep
from PIL import Image

sacred = Doorway()
sacred.bow()

img = Image.open("doorway/res/flames.jpeg")
#img = Image.open("doorway/res/rainbow.jpg")
img = img.resize((29, 2048))
pixels = img.load()

lines = []
for y in range(img.size[1]):
	xs = []
	for x in range(img.size[0]):
		xs.append(pixels[x, y])

	lines.append(xs)


for line in lines:
	count = 0
	for sp in sacred.sheets[1]:
		sacred.pixels[sp[0]] = line[count]
		sacred.pixels[sp[1]] = line[count]
		count += 1	
	sacred.bow()

	count = 0
	for sp in sacred.sheets[2]:
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