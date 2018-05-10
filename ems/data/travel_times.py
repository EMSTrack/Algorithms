from datetime import timedelta

import numpy as np

from ems.models.location import Location
from ems.models.location_set import LocationSet


class TravelTimes:
    """
    Maintains a matrix of travel times between one set of locations to another set of locations
    """
    def __init__(self,
                 loc_set_1: LocationSet,
                 loc_set_2: LocationSet,
                 times: np.ndarray):
        """
        :param loc_set_1:
        :param loc_set_2:
        :param times:
        """
        self.loc_set_1 = loc_set_1
        self.loc_set_2 = loc_set_2
        self.times = times

    def get_time(self, loc1: Location, loc2: Location):
        """
        Retrieves the travel time from the input base and demand point.

        :param loc1:
        :param loc2:
        :return:
        """

        index1 = self.loc_set_1.locations.index(loc1)
        index2 = self.loc_set_2.locations.index(loc2)

        time = int(self.times[index1][index2])

        return timedelta(seconds=time)

