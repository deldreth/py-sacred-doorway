from SimpleCV import *
from doorway.doorway import Doorway
from time import sleep
from collections import deque
from PIL import Image, ImageOps

cam     = Kinect()
display = SimpleCV.Display()

sacred  = Doorway()

while display.isNotDone():
	image    = cam.getDepth().invert()
	pilImage = image.getPIL().rotate(90).resize((28, 7))
	# pilImage = ImageOps.colorize(pilImage, (0, 0, 255), (0, 255, 0))
	pixels   = pilImage.load()

	lines = []
	for y in range(pilImage.size[1]):
		xs = []
		for x in range(pilImage.size[0]):
			xs.append(pixels[x, y])

		lines.append(xs)
		del xs

	deq = deque(maxlen=7)

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

	image.save(display)
