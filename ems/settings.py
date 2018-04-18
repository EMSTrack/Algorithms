# Tells the sim where to look for the data, and whether to enable debug.

class Settings: 

	def __init__ (self, debug=False):
		self.data_filename = None
		self.debug = debug
