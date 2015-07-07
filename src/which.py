from SimpleCV import *
from SimpleCV.Display import *
from collections import deque
from time import sleep

from doorway.doorway import Doorway

import cv
import threading

cam     = Camera()
display = Display((640, 480))

intxors = 0

cameraing = threading.Event()
animating = threading.Event()

def camera (e):
	while not e.is_set():
		print "Camera-ing"

def animate (e, intxors):
	while not e.is_set():
		print "Animating"
		print intxors
		intxors += 1

def which ():
	img = cam.getImage()

	hls = img.toHLS()
	h, l, s = img.splitChannels()
	l = l.threshold(200)

	blobs = l.findBlobs(150, minsize=200)

	print "which called"
	if blobs:
		animating.set()
		cameraing.clear()
		for blob in blobs:
			blob.drawRect(layer=img.dl(), color=Color.GREEN, width=3)
	else:
		cameraing.set()
		animating.clear()

	img.save(display)

	whichT = threading.Timer(1, which)
	whichT.start()
	sleep(1)

cameraing.set()

camT = threading.Thread(target=camera, args=(cameraing,))
aniT = threading.Thread(target=animate, args=(animating, intxors))

camT.daemon = True
aniT.daemon = True

camT.start()
aniT.start()

t = threading.Timer(1, which)
t.start()