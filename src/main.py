#!/usr/bin/python

from doorway.doorway import *
from time import sleep

sacred = Doorway()

pictures = sacred.pics()

print pictures
for pic in pictures:
	print pic
# sacred.bow()

# sleep(0.5)

# sacred.put(1, 255, 0, 0)
# sacred.put(2, 0, 255, 0)
# sacred.put(3, 0, 0, 255)
# sacred.put(4, 255, 255, 0)
# sacred.put(5, 0, 255, 255)
# sacred.put(6, 255, 0, 255)
# sacred.put(7, 255, 255, 255)
# sacred.bow()

# sleep(0.5)

# sacred.pixels = sacred.pixels[::-1]
# sacred.bow()

# for pixel in sacred.sheets[1]:
# 	print pixel
# 	sacred.pixels[pixel[0]] = (255, 0, 0)
# 	sacred.pixels[pixel[1]] = (255, 0, 0)
# 	sacred.bow()
# 	sleep(0.05)

# for pixel in sacred.sheets[2]:
# 	print pixel
# 	sacred.pixels[pixel[0]] = (0, 255, 0)
# 	sacred.pixels[pixel[1]] = (0, 255, 0)
# 	sacred.bow()
# 	sleep(0.05)

# for pixel in sacred.sheets[3]:
# 	print pixel
# 	sacred.pixels[pixel[0]] = (0, 0, 255)
# 	sacred.pixels[pixel[1]] = (0, 0, 255)
# 	sacred.bow()
# 	sleep(0.05)

# for pixel in sacred.sheets[4]:
# 	print pixel
# 	sacred.pixels[pixel[0]] = (255, 255, 0)
# 	sacred.pixels[pixel[1]] = (255, 255, 0)
# 	sacred.bow()
# 	sleep(0.05)

# for pixel in sacred.sheets[5]:
# 	print pixel
# 	sacred.pixels[pixel[0]] = (0, 255, 255)
# 	sacred.pixels[pixel[1]] = (0, 255, 255)
# 	sacred.bow()
# 	sleep(0.05)

# for pixel in sacred.sheets[6]:
# 	print pixel
# 	sacred.pixels[pixel[0]] = (255, 0, 255)
# 	sacred.pixels[pixel[1]] = (255, 0, 255)
# 	sacred.bow()
# 	sleep(0.05)

# for pixel in sacred.sheets[7]:
# 	print pixel
# 	sacred.pixels[pixel[0]] = (255, 255, 255)
# 	sacred.pixels[pixel[1]] = (255, 255, 255)
# 	sacred.bow()
# 	sleep(0.05)