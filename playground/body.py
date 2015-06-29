#!/usr/bin/python

"""
Attempt to get pyXkin working...
"""

from SimpleCV import *
import numpy as np
import sys
sys.path.append("/home/dae/Development/python/pyXKin/xkin")

from xkin.body import BodyDetector

body = BodyDetector()

kinect  = Kinect()
display = Display((640, 480))

while not display.isDone():
	depth = kinect.getDepth()

	bbody = body.run(depth)

	depth.save(display)