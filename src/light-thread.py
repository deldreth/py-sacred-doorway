from SimpleCV import *
from SimpleCV.Display import *
from collections import deque
from time import sleep

from doorway.doorway import Doorway

import cv
import threading

cam     = Camera()
display = Display((640, 480))

sacred = Doorway()
sacred.bow()

deq = deque(maxlen=7)

def draw_images (drawing):
	while not drawing.is_set():	
		print "Drawing..."
		for line in sacred.pics("doorway/res/elements/"):
			deq.append(line)
			sheet_count = 1
			
			for deq_line in deq:
				pix_count = 0
				for l,r in sacred.sheets[sheet_count]:
					
					if drawing.is_set():
						sacred.clear()
						break

					sacred.pixels[l] = deq_line[pix_count]
					sacred.pixels[r] = deq_line[pix_count]
					pix_count += 	1
				
				sacred.bow()

				sheet_count += 1
				sleep(0.01)

drawing = threading.Event()
t1 = threading.Thread(target=draw_images, args=(drawing,))
t1.start()

while display.isNotDone():
	img = cam.getImage()

	hls = img.toHLS() 
	h, l, s = img.splitChannels()
	l = l.threshold(200)

	blobs = l.findBlobs(150, minsize=200)

	if blobs:
		drawing.set()
		for blob in blobs:
			blob.drawRect(layer=l.dl(), color=Color.GREEN, width=3)
	else:
		drawing.clear()
		
	l.save(display)