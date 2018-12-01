from datetime import timedelta

import numpy as np
from geopy import Point

from ems.datasets.location.location_set import LocationSet


class TravelTimes:
    """
    Maintains a matrix of travel travel_times between one set of locations to another set of locations
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

    def get_time(self, location1: Point, location2: Point):
        """
        Retrieves the travel time from the input base and demand point.

        :param location1:
        :param location2:
        :return:
        """

        # TODO implement delta?
        # Find the first location in the first location set
        _, index1, dist1 = self.loc_set_1.closest(location1)
        if dist1 > 0:
            raise Exception("Location 1 does not exist in location set 1")

        # Find the second location in the first location set
        _, index2, dist2 = self.loc_set_2.closest(location2)
        if dist2 > 0:
            raise Exception("Location 2 does not exist in location set 2")

        # TODO check why there is an off by one
        len1 = len(self.times)

        len2 = len(self.times[index1])
        time = int(self.times[index1][index2])

        return timedelta(seconds=time)

