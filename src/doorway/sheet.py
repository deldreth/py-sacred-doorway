#!/usr/bin/python

class Sheet:
	__l= 29 # Pixel length of a sheet

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
		self.__dims['tr'] = 203 + (n * self.__l) - self.__l
		self.__dims['bl'] = self.__dims['tl'] + self.__l
		self.__dims['br'] = self.__dims['tr'] + self.__l

		self.p = p

	def __iter__ (self):
		self.n = 0
		return self

	"""
	Doesn't actually iterate over the 'sheet' just it's pixels
	"""
	def next (self):
		if self.n <= self.__l - 1:
			self.n += 1
			return (self.__dims['tl'] + self.n - 1, self.__dims['tr'] + self.n - 1)
		else:
			raise StopIteration

	def which (self):
		return self.__n

	def set (self, red, green, blue):
		self.p[self.__dims['tl']:self.__dims['bl']] = [(red, green, blue) for x in range(self.__l)]
		self.p[self.__dims['tr']:self.__dims['br']] = [(red, green, blue) for x in range(self.__l)]	

	def dimension (self):
		return self.__dims

	def down (self, sleep):
		return 1