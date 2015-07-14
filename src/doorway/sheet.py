#!/usr/bin/python

class Sheet:
	__l= 28 # Pixel length of a sheet

	def __init__(self, n, p):
		# __dims represends the 'box' like state of a sheet
		self.__dims = {
			'tl': 0, # Top left pixel
			'tr': 0, # Top right pixel
			'bl': 0, # Bottom left pixel
			'br': 0  # Bottom right pixel
		}
		self.__n  = n # Sheet number 1-7

		# Build out the pixel dimensions of the sheet
		self.__dims['tl'] = (n * self.__l) - self.__l
		self.__dims['tr'] = 196 + (n * self.__l) - self.__l
		self.__dims['bl'] = self.__dims['tl'] + self.__l
		self.__dims['br'] = self.__dims['tr'] + self.__l

		self.p = p

	def __iter__ (self):
		self.n = 0
		return self

	def next (self):
		""" Returns sheet dim data from the top down """
		if self.n <= self.__l - 1:
			self.n += 1
			return (self.__dims['tl'] + self.n - 1, self.__dims['tr'] + self.n - 1)
		else:
			raise StopIteration

	def which (self):
		""" Returns the n index for the sheet (1-7) """
		return self.__n

	def set (self, pixels, red, green, blue):
		""" Sets the full sheet to (red, green, blue) """
		pixels[self.__dims['tl']:self.__dims['bl']] = [(red, green, blue) for x in range(self.__l)]
		pixels[self.__dims['tr']:self.__dims['br']] = [(red, green, blue) for x in range(self.__l)]	

		return pixels

	def dimension (self):
		return self.__dims