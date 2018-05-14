# Framework for using algorithms and allowing for replacement
from copy import deepcopy
from typing import List

import numpy as np

from ems.algorithms.analysis.coverage import CoverageAlgorithm
from ems.data.travel_times import TravelTimes
from ems.models.ambulance import Ambulance


# Used by the sim to select ambulances

class DemandCoverage(CoverageAlgorithm):

    def __init__(self,
                 travel_times: TravelTimes):
        self.travel_times = travel_times
        # self._recorded_coverages = []

    def calculate_coverage(self, ambulances: List[Ambulance]):
        """
        At a time, given a list of ambulances, determine the analysis of all the demands.

        :param ambulances:
        :return:
        """

        ambulance_locations = list([amb.base for amb in ambulances if not amb.deployed])
        locations_to_cover = self.travel_times.loc_set_2.locations
        locations_covered = [0 for _ in locations_to_cover]

        for index in range(len(locations_to_cover)):
            loc = locations_to_cover[index]
            if loc:  # TODO I don't know why this is here
                for amb_location in ambulance_locations:
                    if self.travel_times.get_time(amb_location, loc).total_seconds() < 600:
                        locations_covered[index] = 1
                        break



        # total = sum(demands_covered)

        total = sum(locations_covered)

        return total

    # def get_most_recent(self):
    #     return self._recorded_coverages[-1]
    #
    # def get_all_coverages(self):
    #     return deepcopy(self._recorded_coverages)
    #
    # def avg_coverage(self):
    #     """
    #     :return: The average of the coverages so far.
    #     """
    #     avg = sum(self._recorded_coverages) / len(self._recorded_coverages)
    #     return avg
    #
    # def max_coverage(self):
    #     return max(self._recorded_coverages)
    #
    # def min_coverage(self):
    #     return min(self._recorded_coverages)
    #
    # def std_dev_coverage(self):
    #     std_dev = np.std(np.array([time for time in self._recorded_coverages]), axis=0)
    #     return std_dev.item()
