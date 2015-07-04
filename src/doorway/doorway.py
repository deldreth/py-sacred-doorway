from sheet import Sheet
from PIL import Image
from time import sleep
from Queue import Queue

from collections import deque

import opc
import os, sys
import threading

class Doorway (object):
	sheets = {
		1 : 0,
		2 : 0,
		3 : 0,
		4 : 0,
		5 : 0,
		6 : 0,
		7 : 0
	}

	pixels  = [(0, 0, 0) for x in range(392)]
	client  = opc.Client("localhost:7890")

	@classmethod
	def __init__ (self, client = "localhost:7890"):
		self.client = opc.Client(client)

		for s in self.sheets:
			self.sheets[s] = Sheet(s, self.pixels)

		self.bow() # Go ahead and write empty state to opc

	def put (self, sheet, red = 0, green = 0, blue = 0, rgb = (0, 0, 0)):
		if rgb > (0, 0, 0):
			red, green, blue = rgb

		self.sheets[sheet].set(red, green, blue)

	# Write the pixel state to the client
	@classmethod
	def bow (self, tsleep=0):
		self.client.put_pixels(self.pixels, 0)
		sleep(tsleep)

	def clear (self):
		self.pixels = [(0, 0, 0) for x in range(392)]
		self.bow()

	def pics (self, path = "doorway/res/"):
		return DoorwayImages(path).__iter__()


class DoorwayImages (Doorway):
	def __init__ (self, path = "doorway/res/"):
		self.path = os.path.abspath(path) 
		self.imgs = []

		for pic in os.listdir(self.path):
			if os.path.isfile(path+pic):
				img = Image.open(path+pic)
				img = img.resize((28, img.size[1])) # Scale width down to 28 px but leave height alone
				self.imgs.append(img)

				del img # Since we only really care about the pixel data, no sense leaving this around

		self.pixels = self.__pixelize() # We don't really care about the raw image data, just its pixels

	def __iter__ (self):
		return iter(self.pixels)


	def __pixelize(self):
		""" Returns a list of pixel data from self.imags """
		lines = []
		for img in self.imgs:
			pixels = img.load()
			for y in range(img.size[1]):
				xs = []
				for x in range(img.size[0]):
					xs.append(pixels[x, y])

				lines.append(xs)
				del xs	

		del self.imgs

		return lines


class DoorwayAnimations (Doorway, threading.Thread): 
	animations = Queue() # .put({'sheets' : (n,), 'rgb' : (red, green, blue), 'direction' : 'up|down', 'sleep' : n})

	def __init__ (self, q):
		threading.Thread.__init__(self)
		self.animations = q

	def run (self):
		print self.animations.qsize()
		while True:
			animation = self.animations.get()
			
			if animation:
				for sheet in animation['sheets']:
					if 'direction' in animation and animation['direction'] == 'up':
						sheet_pixels = reversed(list(self.sheets[sheet]))
					else:
						sheet_pixels = list(self.sheets[sheet])

					for l, r in sheet_pixels:
						self.pixels[l] = animation['rgb']
						self.pixels[r] = animation['rgb']
						self.bow(animation['sleep'])

			if self.animations.qsize() == 0:
				break