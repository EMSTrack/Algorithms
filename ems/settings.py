# Tells the sim where to look for the data, and whether to enable debug.

class Settings: 

    def __init__ (self, debug=False, demands_file=None, bases_file=None):
        self.data_filename = None
        self.debug = debug
        self.demands_file = demands_file
        self.bases_file = bases_file

    def set_demands_fd (self, filename):
        assert isinstance (filename, str)
        self.demands_file = filename
