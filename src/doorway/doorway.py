from sheet import Sheet
import opc

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

	client = opc.Client('localhost:22000')

	pixels = [(0, 0, 0) for x in range(406)]

	def __init__ (self):
		for s in self.sheets:
			self.sheets[s] = Sheet(s, self.pixels)

	def put (self, sheet, red, green, blue):
		self.sheets[sheet].set(red, green, blue)

	"""
	Write the pixel state to the client
	"""
	def bow (self):
		self.client.put_pixels(self.pixels, 0)

