#!/usr/bin/python
import unittest
from doorway.doorway import *

""" Run from src dir with "python -m unittest discover """

class DoorwayCase (unittest.TestCase):
	def test_init (self):
		doorway = Doorway()

		self.assertEqual(isinstance(doorway, Doorway), True) 

		for sheet in doorway.sheets:
			self.assertEqual(isinstance(doorway.sheets[sheet], Sheet), True)

	def test_pixels (self):
		doorway = Doorway();

		self.assertEqual(len(doorway.pixels), 392)

		for pixels in doorway.pixels:
			self.assertEqual(pixels, (0, 0, 0))

	def test_put (self):
		doorway = Doorway()
		
		doorway.put(1, 255, 0, 0)		
		for l, r in doorway.sheets[1]:
			self.assertEqual(doorway.pixels[l], (255, 0, 0))
			self.assertEqual(doorway.pixels[r], (255, 0, 0))

		doorway.put(1, 0, 255, 0)		
		for l, r in doorway.sheets[1]:
			self.assertEqual(doorway.pixels[l], (0, 255, 0))
			self.assertEqual(doorway.pixels[r], (0, 255, 0))

		for l, r in doorway.sheets[7]:
			self.assertEqual(doorway.pixels[l], (0, 0, 0))
			self.assertEqual(doorway.pixels[r], (0, 0, 0))

	def test_pics (self):
		doorway = Doorway()
		images = doorway.pics("doorway/res/tests/") # One white 28x28 jpg

		self.assertEqual(hasattr(images, '__iter__'), True)

		for image in images:
			self.assertEqual(len(image), 28)

			for line in image:
				self.assertEqual(type(line), tuple)
				self.assertEqual(line, (255, 255, 255))

if __name__ == '__main__':
	unittest.main()