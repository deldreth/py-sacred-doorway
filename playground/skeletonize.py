#!/usr/bin/python

"""
Test to play around with binarize on depth maps as well as
skeletonizing the whole image.
"""

from SimpleCV import *
from SimpleCV.Display import *
from time import sleep

kinect  = Kinect()
display = Display((640, 480))

while display.isNotDone():
    #depth = kinect.getDepth().binarize().dilate()
    depth = kinect.getDepth().binarize().erode(3)

    depth = depth.skeletonize() 

    lines = depth.equalize().findBlobs()
    lines[-1].draw()

    depth.save(display)
    