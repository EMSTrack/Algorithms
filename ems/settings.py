# Tells the sim where to look for the data, and whether to enable debug.

class Settings: 

    # TODO - read from config to generate settings
    def __init__ (self, 
        debug            = False, 
        demands_file     = None, 
        bases_file       = None, 
        cases_file       = None,
        traveltimes_file = None):

        assert demands_file is None  or isinstance (demands_file, str)
        assert bases_file   is None  or isinstance (bases_file, str)
        assert cases_file   is None  or isinstance (cases_file, str)
        assert traveltimes_file is None or isinstance (traveltimes_file, str)

        self.data_filename   = None
        self.debug           = debug
        self.demands_file    = demands_file
        self.bases_file      = bases_file
        self.cases_file      = cases_file
        self.traveltimes_file = traveltimes_file
        self.num_ambulances  = 12 # TODO
        self.num_bases       = 12 # TODO


    def set_demands_fd (self, filename):
        assert isinstance (filename, str)
        self.demands_file = filename

    def set_bases_fd (self, filename):
        assert isinstance (filename, str)
        self.bases_file = filename

    def set_cases_fd (self, filename):
        assert isinstance (filename, str)
        self.cases_file = filename

    def set_traveltimes_fd (self, filename):
        assert isinstance (filename, str)
        self.traveltimes_file = filename