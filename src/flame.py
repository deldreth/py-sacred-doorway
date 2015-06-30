#!/usr/bin/python

from doorway.doorway import Doorway
from time import sleep
from PIL import Image
from collections import deque

sacred = Doorway()
sacred.bow()

sleep(2)

# img = Image.open("doorway/res/flames.jpeg")
# img = img.resize((29, 2048))

#img = Image.open("doorway/res/rainbow.jpg")
#img = img.resize((29, 2048))


#img = Image.open("doorway/res/wedding1.jpg")
#img = img.resize((29, 960))

#img = Image.open("doorway/res/water2.jpg")
#img = img.resize((29, 333))

imgs = []

img = Image.open("doorway/res/chakras/1.jpg")
img = img.resize((29, 29))
imgs.append(img)

img = Image.open("doorway/res/chakras/2.jpg")
img = img.resize((29, 29))
imgs.append(img)

img = Image.open("doorway/res/chakras/3.jpg")
img = img.resize((29, 29))
imgs.append(img)

img = Image.open("doorway/res/chakras/4.jpg")
img = img.resize((29, 29))
imgs.append(img)

img = Image.open("doorway/res/chakras/5.jpg")
img = img.resize((29, 29))
imgs.append(img)

img = Image.open("doorway/res/chakras/6.jpg")
img = img.resize((29, 29))
imgs.append(img)

img = Image.open("doorway/res/chakras/7.jpg")
img = img.resize((29, 29))
imgs.append(img)

lines = []
for img in imgs:
	pixels = img.load()
	for y in range(img.size[1]):
		xs = []
		for x in range(img.size[0]):
			xs.append(pixels[x, y])

		lines.append(xs)
		del xs

deq = deque(maxlen=7)

while True:
	for line in lines:
		deq.append(line)
		sheet_count = 1
		for deq_line in deq:
			pix_count = 0
			for l,r in sacred.sheets[sheet_count]:
				sacred.pixels[l] = deq_line[pix_count]
				sacred.pixels[r] = deq_line[pix_count]
				pix_count += 1
				
			sheet_count += 1
			sacred.bow()
		sleep(0.05)