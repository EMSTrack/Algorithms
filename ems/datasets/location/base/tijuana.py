from ems.datasets.location.base.base_set import BaseSet

class TijuanaBaseSet(BaseSet):

    def __init__(self, filename):
        """ Read the TJ base set, which is the first 8 locations in the bases file. """

        latitudes, longitudes = self.read_bases(filename)
        super().__init__(latitudes=latitudes[0: 8], longitudes=longitudes[0: 8])
