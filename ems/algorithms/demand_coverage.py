# Framework for using algorithms and allowing for replacement
from copy import deepcopy
from datetime import timedelta
from typing import List

import numpy as np

from ems.algorithms.coverage import CoverageAlgorithm
from ems.data.traveltimes import TravelTimes
from ems.models.ambulance import Ambulance


# Used by the sim to select ambulances
class DemandCoverage (CoverageAlgorithm):
    """
        Barebone class. Users may subclass to implement their own ambulance_selection for
        finding coverage.
    """

    def __init__(self, travel_times:TravelTimes):
        self.travel_times:TravelTimes = travel_times
        self._recorded_coverages:List = []


    def calculate_entire_coverage(self, ambulances : List[Ambulance]):
        """
        At a time, given a list of ambulances, determine the coverage of all the demands.

        :param ambulances:
        :return:
        """

        active_bases = list([amb.base for amb in ambulances if not amb.deployed])
        demands = self.travel_times.demands.locations
        # import IPython; IPython.embed()
        demands_covered = [0 for _ in demands]

        for index in range(len(demands)):
            if demands[index]: # TODO I don't know why this ishere
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





    def avgCoverage(self):
        """

        :return: The average of the coverages so far.
        """
        avg = sum(self._recorded_coverages) / len(self._recorded_coverages)
        return avg

    def maxCoverage(self):
        return max(self._recorded_coverages)

    def minCoverage(self):
        return min(self._recorded_coverages)

    def stdDevCoverage(self):
        std_dev = np.std(np.array([time.total_seconds() for time in self._recorded_coverages]), axis=0)
        return timedelta(std_dev.item())
