from sheet import Sheet

from PIL import Image
from time import sleep, time
from collections import deque

import opc
import os, sys
import random

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

	gamma = bytearray(256)

	# pixels  = [(0, 0, 0) for x in range(392)]
	#client  = opc.Client("localhost:7890")

	def __init__ (self, client = "localhost:7890"):
		self.client = opc.Client(client)
		self.pixels = [(0, 0, 0) for x in range(392)]

		for s in self.sheets:
			self.sheets[s] = Sheet(s, self.pixels)

		self.gamma = self.gamma_table()

		self.bow() # Go ahead and write empty state to opc

	def put (self, sheet, red = 0, green = 0, blue = 0, rgb = (0, 0, 0)):
		if rgb > (0, 0, 0):
			red, green, blue = rgb

		self.sheets[sheet].set(red, green, blue)

	# Write the pixel state to the client
	def bow (self, tsleep=0):
		self.client.put_pixels(self.pixels, 0)
		sleep(tsleep)

	def clear (self):
		self.pixels = [(0, 0, 0) for x in range(392)]
		self.bow()

	def get_sheets(self):
		return self.sheets

	def get_pixels(self):
		return self.pixels

	def set_pixel(self, index, value):
		self.pixels[index] = value;

	@classmethod
	def rand_color (self):
		return (random.randrange(255), random.randrange(255), random.randrange(255))

	@classmethod
	def nog_color_wheel(self, value):
		""" Given 0-255, make an rgb color without gamma correction """
		if value < 85:
			return (value * 3, 255 - value * 3, 0)
		elif value < 170:
			value -= 85
			return (255 - value * 3, 0, value * 3)
		else:
			value -= 170
			return (0, value * 3, 255 - value * 3)

	@classmethod
	def color_wheel(self, value):
		""" Given 0-255, make an rgb color with gamma correction """
		if value < 85:
			return (self.gamma[value * 3], self.gamma[255 - value * 3], 0)
		elif value < 170:
			value -= 85
			return (self.gamma[255 - value * 3], 0, self.gamma[value * 3])
		else:
			value -= 170
			return (0, self.gamma[value * 3], self.gamma[255 - value * 3])

	def gamma_table (self):
		for i in range(256):
			Doorway.gamma[i] = int(pow(float(i) / 255.0, 2.7) * 255.0 + 0.5)

		return Doorway.gamma



class DoorwayEffects (Doorway):
	"""
		strobe_*    - Just that, it strobes all the sheets
		FtoB & BtoF - Front to Back, Back to Front
		rainbow_*   - Uses @Doorway.color_wheel to create rainbow effects
		timed_      - Time is involved in some way
		wipe_       - "wipes" a color up|down on a sheet
	"""

	#renderable = True

	def __init__ (self):
		super(DoorwayEffects, self).__init__()
		self.renderable = True

	def set_renderable(self, renderable):
		self.renderable = renderable

	def get_renderable(self):
		return self.renderable

	def all_black (self):
		for sheet in range(1,8):
			self.put(sheet, rgb=(0, 0, 0))
		self.bow()

	def strobe_FtoB (self, times=10, tsleep=0.01, color1=(255, 255, 255), color2=(0, 0, 0)):
		for sheet in range(1,8):
			for n in range(times):
				if not self.renderable:
					return True

				self.put(sheet, rgb=color1)
				self.bow(tsleep)
				self.put(sheet, rgb=color2)
				self.bow(tsleep)

	def strobe_BtoF (self, times=10, tsleep=0.01, color1=(255, 255, 255), color2=(0, 0, 0)):
		for sheet in reversed(range(1,8)):
			for n in range(times):
				if not self.renderable:
					return True

				self.put(sheet, rgb=color1)
				self.bow(tsleep)
				self.put(sheet, rgb=color2)
				self.bow(tsleep)

	def strobe_rainbow_FtoB (self, tsleep=0.1):
		for color in range(1, 250, 20):
			for sheet in range(1,8):
				if not self.renderable:
					return True

				self.put(sheet, rgb=Doorway.color_wheel(color))
				self.bow(tsleep)
				self.put(sheet, rgb=(0, 0, 0))
				self.bow(tsleep)

	def strobe_rainbow_BtoF (self, tsleep=0.1):
		for color in range(1, 250, 20):
			for sheet in reversed(range(1,8)):
				if not self.renderable:
					return True

				self.put(sheet, rgb=Doorway.color_wheel(color))
				self.bow(tsleep)
				self.put(sheet, rgb=(0, 0, 0))
				self.bow(tsleep)

	def rainbow_FtoB (self, tsleep=0.1):
		for color in range(1, 250, 20):
			for sheet in range(1,8):
				if not self.renderable:
					return True

				self.put(sheet, rgb=Doorway.color_wheel(color))
				self.bow(tsleep)

	def rainbow_BtoF (self, tsleep=0.1):
		for color in range(1, 250, 20):
			for sheet in reversed(range(1,8)):
				if not self.renderable:
					return True

				self.put(sheet, rgb=Doorway.color_wheel(color))
				self.bow(tsleep)

	def timed_rainbow_FtoB (self):
		for color in range(1, 250, 10):
			for sheet in range(1,8):
				for ti in range(1, 30):
					if not self.renderable:
						return True

					self.put(sheet, rgb=Doorway.color_wheel(color))
					self.bow(ti/30)

	def timed_rainbow_BtoF (self):
		for color in range(1, 250, 10):
			for sheet in reversed(range(1,8)):
				for ti in range(1, 30):
					if not self.renderable:
						return True

					self.put(sheet, rgb=Doorway.color_wheel(color))
					self.bow(ti/30)

	def wipe_down (self, sheet, color=(255, 255, 255), tsleep=0.01):
		for l, r in self.sheets[sheet]:
			if not self.renderable:
				return True

			self.pixels[l] = color
			self.pixels[r] = color
			self.bow(tsleep)

	def wipe_up (self, sheet, color=(255, 255, 255), tsleep=0.01):
		for l, r in reversed(list(self.sheets[sheet])):
			if not self.renderable:
				return True

			self.pixels[l] = color
			self.pixels[r] = color
			self.bow(tsleep)

	def wipe_left_down (self, color=(255, 255, 255), tsleep=0.05):
		for sheet in self.sheets:
			for l, r in self.sheets[sheet]:
				if not self.renderable:
					return True

				self.pixels[l] = color
				self.bow(tsleep)

	def swipe_up (self, color=(255, 255, 255), tsleep=0.05):
		dims = []

		for sheet in self.sheets:
			dims.append(self.sheets[sheet].dimension())

		for pixel in range(28):
			for dim in dims:
				bl = dim['bl'] - pixel - 1
				br = dim['br'] - pixel - 1
				self.pixels[bl] = color
				self.pixels[br] = color
			
			self.bow(tsleep)

	def swipe_down (self, color=(255, 255, 255), tsleep=0.05):
		dims = []

		for sheet in self.sheets:
			dims.append(self.sheets[sheet].dimension())

		for pixel in range(28):
			for dim in dims:
				tl = dim['tl'] + pixel
				tr = dim['tr'] + pixel
				self.pixels[tl] = color
				self.pixels[tr] = color
			
			self.bow(tsleep)

	def images (self, path, tsleep=0.01):
		path = os.path.abspath(path)
		imgs = []

		for pic in sorted(os.listdir(path)):
			if os.path.isfile(path+'/'+pic):
				img = Image.open(path+'/'+pic)
				img = img.resize((28, img.size[1])) # Scale width down to 28 px but leave height alone
				#img = img.resize((28, 28))
				imgs.append(img)

				del img # Since we only really care about the pixel data, no sense leaving this around

		lines = self.__pixelize(imgs)

		deq  = deque(maxlen = 7)
		for line in lines:
			deq.append(line)
			sheet_count = 7

			for deq_line in deq:
				pix_count = 0
				for l,r in self.sheets[sheet_count]:
					if not self.renderable:
						return True

					self.pixels[l] = deq_line[pix_count]
					self.pixels[r] = deq_line[pix_count]
					pix_count += 1

				sheet_count -= 1
			self.bow(tsleep)

	def picture (self, path, tsleep=(0.01)):
		path = os.path.abspath(path)

		if os.path.isfile(path):
			img = Image.open(path)
			img = img.resize((28,28))

			lines = self.__pixelize([img])

			deq  = deque(maxlen = 7)
			for line in lines:
				deq.append(line)
				sheet_count = 7

				for deq_line in deq:
					pix_count = 0
					for l,r in self.sheets[sheet_count]:
						if not self.renderable:
							return True

						self.pixels[l] = deq_line[pix_count]
						self.pixels[r] = deq_line[pix_count]
						pix_count += 1

					sheet_count -= 1
				self.bow(tsleep)

	def __pixelize(self, images):
		""" Returns a list of pixel data """
		lines = []
		for img in images:
			pixels = img.load()
			for y in range(img.size[1]):
				xs = []
				for x in range(img.size[0]):
					xs.append(pixels[x, y])

				lines.append(xs)
				del xs

		del images

		return lines