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

        self.ls1_map = {}
        for index, key1 in enumerate(loc_set_1.locations):
            self.ls1_map[key1.id] = index

        self.ls2_map = {}
        for index, key2 in enumerate(loc_set_2.locations):
            self.ls2_map[key2.id] = index

    def get_time(self, loc1: Location, loc2: Location):
        """
        Retrieves the travel time from the input base and demand point.

        :param loc1:
        :param loc2:
        :return:
        """

        index1 = self.ls1_map[loc1.id]
        index2 = self.ls2_map[loc2.id]

        time = int(self.times[index1][index2])

        return timedelta(seconds=time)

