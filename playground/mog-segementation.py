#!/usr/bin/python

from SimpleCV import *
from SimpleCV.Display import *
from time import sleep

kinect  = Kinect()
display = Display((640, 480))

pdepth = kinect.getDepth().invert()

ds = MOGSegmentation(history = 500, nMixtures = 5, backgroundRatio = 0.1, noiseSigma = 5, learningRate = 0.3)
ds.addImage(pdepth)

while not display.isDone():
    depth = kinect.getDepth()
    ds.addImage(depth)

    df = ds.getSegmentedImage(False)

    """
    if df is not None:
        print "diffed"
        blobs = df.dilate(3).findBlobs()

        if blobs is not None:
            df.dl().polygon(blobs[-1].mConvexHull, color = Color.RED)   
    """

    df.save(display)    

    if display.mouseLeft:
        display.done = True
        del kinect
        #pg.quit()          