import pandas as pd
from datetime import timedelta

import numpy as np
from geopy import Point

from ems.datasets.location.location_set import LocationSet


class TravelTimes:
    """
    Maintains a matrix of travel travel_times between one set of locations to another set of locations
    """
    def __init__(self,
                 origins: LocationSet,
                 destinations: LocationSet,
                 filename: str = None,
                 times: np.ndarray = None):
        """
        :param origins:
        :param destinations:
        :param times:
        """
        self.origins = origins
        self.destinations = destinations

        if filename is not None:
            times = self.read_times_df(filename)

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
        _, index1, dist1 = self.origins.closest(location1)
        if dist1 > 0:
            raise Exception("Location 1 does not exist in location set 1")

        # Find the second location in the first location set
        _, index2, dist2 = self.destinations.closest(location2)
        if dist2 > 0:
            raise Exception("Location 2 does not exist in location set 2")

        time = int(self.times[index1][index2])

        return timedelta(seconds=time)

    def read_times_df(self, filename):
        # Read travel travel_times from CSV file into a pandas dataframe
        travel_times_df = pd.read_csv(filename)

        return travel_times_df.as_matrix()
