from datetime import timedelta

import pandas as pd

# Wrapper class around a travel times data frame

class TravelTimes:

    def __init__(self, times: pd.DataFrame):
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
        time = int(self.times.iloc[base.id][demand.id])

        return timedelta(seconds=time)

