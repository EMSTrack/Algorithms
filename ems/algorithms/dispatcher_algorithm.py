# The following functions define default algorithms for the DispatchAlgorithm class.
import numpy as np
from datetime import timedelta
from typing import List

from ems.algorithms.algorithm import Algorithm
from ems.data.traveltimes import TravelTimes
from ems.models.ambulance import Ambulance
from ems.models.case import Case
from ems.models.demand import Demand
from ems.utils import closest_distance


# An implementation of a "fastest travel time" algorithm from a base to
# the demand point closest to a case

class DispatcherAlgorithm(Algorithm):

    def __init__(self, traveltimes: TravelTimes = None):
        self.traveltimes = traveltimes

    def select_ambulance(self,
                         ambulances: List[Ambulance],
                         case: Case,
                         demands: List[Demand]):

        # Find the closest demand point to the given case
        if case.closest_demand is None:
            case.closest_demand = closest_distance(demands, case.location)

        # Select an ambulance to attend to the given case and obtain the its duration of travel
        chosen_ambulance, ambulance_travel_time = self.find_fastest_ambulance(
            ambulances, self.traveltimes, case.closest_demand)

        return chosen_ambulance, ambulance_travel_time

    def find_fastest_ambulance(self, ambulances, traveltimes, demand):
        """
        Finds the ambulance
        :param ambulances:
        :param traveltimes:
        :param demand:
        :return: type int the ID of the ambulance, or None if all ambulances are busy.
        """

        shortest_time = timedelta(hours=9999999)
        position = -1

        for index, amb in enumerate(ambulances):
            if not amb.deployed:
                time = self.find_traveltime(traveltimes, amb.base, demand)
                if shortest_time > time:
                    shortest_time = time
                    position = index

        if position > -1:
            return position, shortest_time

        return None, None

    def find_traveltime(self, traveltimes, base, demand):
        """
        Takes the travel time mapping, starting base, and ending demand to find time.
        :param base:
        :param demand:
        :return travel time:
        """

        # base should be a base object
        # demand should be a demand object

        return traveltimes.get_time(base, demand)
