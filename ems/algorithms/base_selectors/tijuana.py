from ems.algorithms.base_selectors.selector import AmbulanceBaseSelector
from ems.datasets.location.location_set import LocationSet


class TijuanaBaseSelector(AmbulanceBaseSelector):
    """ Based on the original Dibene paper. """

    def __init__(self,
                 base_set: LocationSet):
        self.base_set = base_set

    def select(self, num_ambulances):
        """ This returns list of bases that each ambulance will reside at.  """
        no_ambulances = [-6]
        one_ambulances = [i for i in range(-8, 0) if i not in no_ambulances]
        two_ambulances = [-8, -7, -4, -1]

        ambulances = one_ambulances + two_ambulances

        bases = []

        for base_index in ambulances:
            bases.append(self.base_set.locations[base_index])

        if len(bases) != num_ambulances:
            raise Exception("Wrong number of bases were being assigned to ambulances.")

            # To map the 8 bases.
        from matplotlib import pyplot as plt
        import numpy as np

        # latitudes = [i.latitude for i in bases]
        # longitudes = [i.longitude for i in bases]
        # print("len: " , len(latitudes))

        # lat2 = [self.base_set.locations[i].latitude for i in two_ambulances]
        # lon2 = [self.base_set.locations[i].longitude for i in two_ambulances]
        #
        # print(np.array([(latitudes, longitudes) ]))
        # print("Length chosen: ", len(latitudes))
        # print("Length doubled: ", len(lat2))
        # plt.plot(longitudes, latitudes, "o")
        # plt.plot(lon2, lat2, '*')
        # plt.plot()
        # plt.show()

        return bases
