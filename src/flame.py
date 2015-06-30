#!/usr/bin/python

from doorway.doorway import Doorway
from time import sleep
from PIL import Image

sacred = Doorway()
sacred.bow()

img = Image.open("doorway/res/flames.jpeg")
img = img.resize((29, 2048))
pixels = img.load()

lines = []
for y in range(img.size[1]):
	xs = []
	for x in range(img.size[0]):
		xs.append(pixels[x, y])

	lines.append(xs)

for line in lines:
	for sp in sacred.sheets[1]:
		for pixel in line:
			sacred.pixels[sp[0]] = pixel
			sacred.pixels[sp[1]] = pixel
	for sp in sacred.sheets[2]:
		for pixel in line:
			sacred.pixels[sp[0]] = pixel
			sacred.pixels[sp[1]] = pixel
	for sp in sacred.sheets[3]:
		for pixel in line:
			sacred.pixels[sp[0]] = pixel
			sacred.pixels[sp[1]] = pixel

		sacred.bow()
		sleep(0.001)