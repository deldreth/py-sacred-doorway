#!/usr/bin/python

from SimpleCV import *
from SimpleCV.Display import *
from time import sleep

kinect  = Kinect()
display = Display((640, 480))

while not display.isDone():
    depth = kinect.getImage().stretch(10)
    
    bodies = depth.findHaarFeatures(LAUNCH_PATH + '/Features' + '/HaarCascades' + '/upper_body2.xml')

    if bodies:
        print "Upper Body Detected"
        
        body = bodies.sortArea()[-1]
        body.draw(width=5)
        print body
        depth.save(display)
        
        """ 
        blobs = body.findBlobs(threshval=-1, minsize=10, maxsize=0)

        if blobs:
            for blob in blobs:
                blob.drawHull(color=Color.RED,width=3,alpha=128)
        """
        

    depth.save(display)     
    