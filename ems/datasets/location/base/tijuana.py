from ems.datasets.location.base.base_set import BaseSet

class TijuanaBaseSet(BaseSet):

    def __init__(self, filename):
        """ Read the TJ base set, which is the first 8 locations in the bases file. """

        latitudes, longitudes = self.read_bases(filename)

        # To map the 8 bases.
        from matplotlib import pyplot as plt
        import numpy as np

        # print(np.array([(latitudes[i], longitudes[i]) for i in range(-8, 0)]))
        # plt.plot(longitudes[-8: ], latitudes[-8: ], "o")
        # plt.show()

        super().__init__(latitudes=latitudes[-8:], longitudes=longitudes[-8:])
