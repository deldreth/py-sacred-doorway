#!/usr/bin/python

"""
Given example of tracking optical flow with a standard camera
"""

from SimpleCV import *

def movement_check(x = 0,y = 0,t=1):
    print (x, y, t)
    direction = ""
    directionX = ""
    directionY = ""
    if x > t:
        directionX = "Right"
    if x < -1*t:
        directionX = "Left"
    if y < -1*t:
        directionY = "Up"
    if y > t:
        directionY = "Down"

    direction = directionX + " " + directionY
    if direction is not "":
        return direction
    else:
        return "No Motion"

def main():
    scale_amount = (200,150)
    d = Display(scale_amount)
    cam = Camera(0)
    prev = cam.getImage().scale(scale_amount[0],scale_amount[1])
    #time.sleep(0.5)
    t = 0
    buffer = 20
    count = 0
    while d.isNotDone():
        current = cam.getImage()
        current = current.scale(scale_amount[0],scale_amount[1])
        if( count < buffer ):
            count = count + 1
        else:
            fs = current.findMotion(prev, window=15, method="BM", aggregate=True)
            lengthOfFs = len(fs)
            print lengthOfFs
            if fs:
                dx = 0
                dy = 0
                for f in fs:
                    dx = dx + f.dx
                    dy = dy + f.dy

                dx = (dx / lengthOfFs)
                dy = (dy / lengthOfFs)
                motionStr = movement_check(dx,dy,t)
                current.drawText(motionStr,10,10)

        prev = current
        time.sleep(0.01)
        current.save(d)

if __name__ == '__main__':
    main()