# Tells the sim where to look for the data, and whether to enable debug.

class Settings: 

    # TODO - read from config to generate settings
    def __init__ (self, 
        debug: str            = False, 
        demands_file: str     = None, 
        bases_file: str       = None, 
        cases_file: str       = None,
        traveltimes_file: str = None,
        amortized_file: str   = None):

        self.data_filename      = None
        self.debug              = debug
        self.demands_file       = demands_file
        self.bases_file         = bases_file
        self.cases_file         = cases_file
        self.traveltimes_file   = traveltimes_file
        self.amortized_file     = amortized_file
        self.num_ambulances     = 12 # TODO
        self.num_bases          = 12 # TODO