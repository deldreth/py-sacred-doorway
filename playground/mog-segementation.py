#!/usr/bin/python

from SimpleCV import *
from SimpleCV.Display import *
from time import sleep

kinect  = Kinect()
display = Display((640, 480))

pdeth = kinect.getDepth()

ds = MOGSegmentation()
ds.addImage(pdeth)

while not display.isDone():
	depth = kinect.getDepth()
	ds.addImage(depth)

	df = ds.getSegmentedImage(False)

	if df is not None:
		print "diffed"
		blobs = df.dilate(3).findBlobs()

		if blobs is not None:
			depth.dl().polygon(blobs[-1].mConvexHull, color = Color.RED)	

	depth.save(display)					
