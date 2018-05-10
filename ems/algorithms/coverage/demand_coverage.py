# Framework for using algorithms and allowing for replacement
from copy import deepcopy
from typing import List

import numpy as np

from ems.algorithms.coverage.coverage import CoverageAlgorithm
from ems.data.travel_times import TravelTimes
from ems.models.ambulance import Ambulance


# Used by the sim to select ambulances

class DemandCoverage(CoverageAlgorithm):

    def __init__(self,
                 travel_times: TravelTimes):
        self.travel_times = travel_times
        self._recorded_coverages = []

    def calculate_coverage(self, ambulances: List[Ambulance]):
        """
        At a time, given a list of ambulances, determine the coverage of all the demands.

        :param ambulances:
        :return:
        """

        active_bases = list([amb.base for amb in ambulances if not amb.deployed])
        demands = self.travel_times.loc_set_2.locations
        demands_covered = [0 for _ in demands]

        for index in range(len(demands)):
            if demands[index]:  # TODO I don't know why this is here
                for base in active_bases:
                    dem = demands[index]
                    if self.travel_times.get_time(base, dem).total_seconds() < 600:
                        demands_covered[index] = 1
                        break

        total = sum(demands_covered)
        self._recorded_coverages.append(total)
        return total

    def get_most_recent(self):
        return self._recorded_coverages[-1]

    def get_all_coverages(self):
        return deepcopy(self._recorded_coverages)

    def avg_coverage(self):
        """
        :return: The average of the coverages so far.
        """
        avg = sum(self._recorded_coverages) / len(self._recorded_coverages)
        return avg

    def max_coverage(self):
        return max(self._recorded_coverages)

    def min_coverage(self):
        return min(self._recorded_coverages)

    def std_dev_coverage(self):
        std_dev = np.std(np.array([time for time in self._recorded_coverages]), axis=0)
        return std_dev.item()
