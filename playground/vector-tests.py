#!/usr/bin/python

from SimpleCV import *
from SimpleCV.Display import *
from time import sleep

kinect  = Kinect()
display = Display((640, 480))

ds = MOGSegmentation(history = 200, nMixtures = 50, backgroundRatio = 0.1, noiseSigma = 5, learningRate = 0.6)

# An 'original' to compare for motion detection
pdepth = kinect.getDepth()
ds.addImage(pdepth.binarize())

while not display.isDone():
	depth = kinect.getDepth()
	depth.stretch(0, 25)
	depth = depth.binarize()

	ds.addImage(depth)

	df = ds.getSegmentedImage(False)

	blobs = depth.findBlobs(threshval=-1, minsize=10, maxsize=0)
	
	"""
	Track motion over the depth frames. It's slow and computes hundreds
	of motion vectors at a time.
	motion = depth.findMotion(pdepth, window = (640, 480), aggregate=True)
	for m in range(10):
		if motion[m].magnitude() > 100.0:
			dx, dy = motion[m].vector()
			
			if dx > 150:
				print "Right"
			elif dx < 150: 
				print "Left"
			
			m.draw(color=Color.RED, normalize=True)
	"""
		
	if blobs:
		for blob in blobs:
			blob.drawHull(color=Color.GREEN,width=3,alpha=128)
			blob.draw(color=Color.RED)
			blob.drawHoles(color=Color.RED)           
			depth.drawCircle((blob.contour()[-1]),10,color=Color.BLUE)
		
	depth.save(display)
	sleep(0)

	pdepth = depth
