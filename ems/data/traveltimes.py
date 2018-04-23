from datetime import timedelta

import pandas as pd


# TODO -- instead of a model, make a travel time set object
class TravelTime:

    def __init__(self, base_id: int, demand_id: int, traveltime: timedelta):
        self.base_id = base_id
        self.demand_id = demand_id
        self.traveltime = traveltime


class TravelTimeSet:

    def __init__(self, times: pd.DataFrame):
        """

        :type times: object
        """
        self.times = times

    def get_time(self, base, demand):
        """

        :param base:
        :param demand:
        :return:
        """
        # return self.times[base.id][demand.id]
        pass

