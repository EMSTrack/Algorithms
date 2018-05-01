from datetime import timedelta

import numpy as np


# Wrapper class around a travel times data frame

class TravelTimes:

    def __init__(self, times: np.ndarray):
        """

        :type times: Pandas dataframe
        """
        self.times = times

    def get_time(self, base, demand):
        """
        Retrieves the travel time from the input base and demand point.

        :param base:
        :param demand:
        :return:
        """
        time = int(self.times[base.id][demand.id])

        return timedelta(seconds=time)

