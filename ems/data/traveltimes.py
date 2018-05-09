from datetime import timedelta

from typing import Type

from ems.models.location_set import LocationSet
from scipy.spatial import KDTree
from ems.models.base import Base
from ems.models.case import Demand
from geopy import Point
import numpy as np



class TravelTimes:
    """

    """

    def __init__(self, bases:LocationSet, demands:LocationSet, times: np.ndarray):
        """

        :param bases:
        :param demands:
        :param times:
        """

        # import IPython; IPython.embed()
        self.bases:LocationSet = bases
        self.demands:LocationSet = demands
        self.times:np.ndarray = times



    def get_time(self, base:Base, demand:Demand):
        """
        Retrieves the travel time from the input base and demand point.

        :param base:
        :param demand:
        :return:
        """
        time = int(self.times[base.id][demand.id])

        return timedelta(seconds=time)


    def find_nearest_base(self, target_point:Point):
        return self.bases.closest(target_point)[0]

    def find_nearest_demand(self, target_point:Point):
        return self.demands.closest(target_point)[0]

