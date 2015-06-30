#!/usr/bin/python

from doorway.doorway import Doorway
from time import sleep
from PIL import Image
from collections import deque

sacred = Doorway()
sacred.bow()

sleep(1)

img = Image.open("doorway/res/flames.jpeg")
img = img.resize((29, 2048))

#img = Image.open("doorway/res/rainbow.jpg")
#img = img.resize((29, 2048))


#img = Image.open("doorway/res/wedding1.jpg")
#img = img.resize((29, 960))

#img = Image.open("doorway/res/water2.jpg")
#img = img.resize((29, 333))

"""
img = Image.open("doorway/res/metatron.jpg")
img = img.resize((29, 1080))
"""

pixels = img.load()

lines = []
for y in range(img.size[1]):
	xs = []
	for x in range(img.size[0]):
		xs.append(pixels[x, y])

	lines.append(xs)
	del xs

deq = deque(maxlen=7)

sheet = 1
for line in lines:

	if sheet > 7:
		sheet = 1

	deq.append(sheet)
	sheet += 1

	for sheet_deq in deq:
		count = 0

		for l, r in sacred.sheets[sheet_deq]:
			sacred.pixels[l] = line[count]
			sacred.pixels[r] = line[count]
			count += 1

	sacred.bow()
	sleep(0.05)

	"""
	for l, r in sacred.sheets[sheet]:
		sacred.pixels[l] = line[count]
		sacred.pixels[r] = line[count]
		count += 1

	sacred.bow()
	"""

	print deq