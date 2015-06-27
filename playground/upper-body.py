#!/usr/bin/python

from SimpleCV import *
from SimpleCV.Display import *
from time import sleep

kinect  = Kinect()
display = Display((640, 480))

while not display.isDone():
	depth = kinect.getDepth()
	#depth.listHaarFeatures()
	body  = depth.findHaarFeatures(LAUNCH_PATH + '/Features' + '/HaarCascades' + '/upper_body.xml')

	if body is not None:
		print "Upper Body Detected"

		"""
		blobs = body.findBlobs(threshval=-1, minsize=10, maxsize=0)

		if blobs:
			for blob in blobs:
				blob.drawHull(color=Color.RED,width=3,alpha=128)
		"""

	depth.save(display)		
	