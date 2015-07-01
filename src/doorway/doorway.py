from sheet import Sheet
from PIL import Image

import opc
import os, sys

class Doorway:
	sheets = {
		1 : 0,
		2 : 0,
		3 : 0,
		4 : 0,
		5 : 0,
		6 : 0,
		7 : 0
	}

	pixels = [(0, 0, 0) for x in range(392)]

	def __init__ (self, client = "localhost:7890"):
		self.client = opc.Client(client)

		for s in self.sheets:
			self.sheets[s] = Sheet(s, self.pixels)

		self.bow() # Go ahead and write empty state to opc

	def put (self, sheet, red, green, blue):
		self.sheets[sheet].set(red, green, blue)

	# Write the pixel state to the client
	def bow (self):
		self.client.put_pixels(self.pixels, 0)

	def pics(self, path = "doorway/res/"):
		return DoorwayPics(path).__iter__()


class DoorwayPics (Doorway):
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