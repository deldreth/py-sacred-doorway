from SimpleCV import *
from SimpleCV.Display import *
import cv

cam     = Camera()
display = Display((640, 480))


while display.isNotDone():
	img = cam.getImage()

	hls = img.toHLS() # it's also possible to luma from toYCrCb() with the Y channel being luma, and Y' (gamma correctted) being luminance 
	h, l, s = img.splitChannels()
	l = l.threshold(200)

	blobs = l.findBlobs(150, minsize=100)

	if blobs:
		for blob in blobs:
			#l = blob.getFullHullMaskedImage()
			blob.drawRect(layer=img.dl(), color=Color.GREEN, width=3)
		
	img.save(display)