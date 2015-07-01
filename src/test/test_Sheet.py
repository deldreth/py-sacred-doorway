#!/usr/bin/python
import unittest
from doorway.doorway import *

class SheetCase (unittest.TestCase):
	def test_init (self):
		doorway = Doorway()
		
		for sheet in doorway.sheets:
			self.assertEquals(isinstance(doorway.sheets[sheet], Sheet), True)
			self.assertEquals(doorway.sheets[sheet].p, doorway.pixels)

	def test_which (self):
		doorway = Doorway()

		for n in doorway.sheets:
			sheet = doorway.sheets[n]
			self.assertEquals(sheet.which(), n)

	def test_dims (self):
		doorway = Doorway()

		dims = doorway.sheets[1].dimension()		
		self.assertEqual(cmp(dims, {'bl': 28, 'tl': 0, 'tr': 196, 'br': 224}), 0)

		dims = doorway.sheets[2].dimension()		
		self.assertEqual(cmp(dims, {'bl': 56, 'tl': 28, 'tr': 224, 'br': 252}), 0)

		dims = doorway.sheets[3].dimension()
		self.assertEqual(cmp(dims, {'bl': 84, 'tl': 56, 'tr': 252, 'br': 280}), 0)

		dims = doorway.sheets[4].dimension()		
		self.assertEqual(cmp(dims, {'bl': 112, 'tl': 84, 'tr': 280, 'br': 308}), 0)

		dims = doorway.sheets[5].dimension()		
		self.assertEqual(cmp(dims, {'bl': 140, 'tl': 112, 'tr': 308, 'br': 336}), 0)

		dims = doorway.sheets[6].dimension()		
		self.assertEqual(cmp(dims, {'bl': 168, 'tl': 140, 'tr': 336, 'br': 364}), 0)

		dims = doorway.sheets[7].dimension()		
		self.assertEqual(cmp(dims, {'bl': 196, 'tl': 168, 'tr': 364, 'br': 392}), 0)
