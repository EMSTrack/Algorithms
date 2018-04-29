# The following functions define default algorithms for the DispatchAlgorithm class.
from datetime import timedelta
from typing import List

from ems.algorithms.algorithm import Algorithm
from ems.data.traveltimes import TravelTimes
from ems.models.ambulance import Ambulance
from ems.models.case import Case
from ems.models.demand import Demand


# An implementation of a "fastest travel time" algorithm from a base to
# the demand point closest to a case
from ems.utils import closest_distance


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
        chosen_ambulance, ambulance_travel_time = self.find_available_ambulance(
            ambulances, self.traveltimes, case.closest_demand)

        return chosen_ambulance, ambulance_travel_time

    def find_available_ambulance(self, ambulances, traveltimes, demand):
        """
        Find an available ambulance if possible.
        :param ambulances: of type dictionary.
        :param traveltimes:
        :param demand:
        :return: type int the ID of the ambulance, or None if all ambulances are busy.
        """

        ambulance_bases = [a.base if not a.deployed else None for a in ambulances]
        # print('Length of ambulance locations:', len(ambulance_locations))
        # print('FA:', ambulance_locations)
        result, case_time = self.closest_time(ambulance_bases, traveltimes, demand)
        # print('Position:',result)
        if result > -1:
            return result, case_time

        # for amb in ambulances:
        #     if amb['deployed'] == False:
        #         distance =

        return None, None

    def closest_time(self, list_type, traveltimes, demand):
        """
        Finds the ambulance, given a list of ambulances, that will reach the
        demand point the closest. The demand point must be in the list of demands.
        IF it is not, then use the above function `closest_distance` to find the
        closest demand point given a GPS coordinate.
        The parameter names are bad and the code needs to be refactored, probably
        :param list_type:
        :param traveltimes:
        :param demand:
        :return:
        """
        shortest_difference = timedelta(hours=999999999)
        position = -1
        for index in range(len(list_type)):

            if list_type[index] is not None:

                difference = self.traveltime(traveltimes, list_type[index], demand)
                if shortest_difference > difference:
                    shortest_difference = difference
                    position = index

        return position, shortest_difference

    def traveltime(self, traveltimes, base, demand):
        """
        Takes the travel time mapping, starting base, and ending demand to find time.
        :param base:
        :param demand:
        :return travel time:
        """

        # base should be a base object
        # demand should be a demand object

        return traveltimes.get_time(base, demand)
