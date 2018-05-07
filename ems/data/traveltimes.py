from datetime import timedelta

from ems.models.location_set import LocationSet
import numpy as np


# Wrapper class around a travel times data frame

class TravelTimes:

    def __init__(self, bases:LocationSet, demands:LocationSet, times: np.ndarray):
        """

        :type times: Pandas dataframe
        """
        self.bases = bases
        self.demands = demands
        self.times = times

        #TODO
        # self.kd_tree = self.initialize_kd_tree(demands)

    def get_time(self, base, demand):
        """
        Retrieves the travel time from the input base and demand point.

        :param base:
        :param demand:
        :return:
        """
        time = int(self.times[base.id][demand.id])

        return timedelta(seconds=time)

