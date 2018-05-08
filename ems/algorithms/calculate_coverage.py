# Framework for using algorithms and allowing for replacement
from typing import List

from ems.models.ambulance import Ambulance
from ems.models.location_set import LocationSet

from ems.algorithms.coverage import CoverageAlgorithm

import numpy as np
from datetime import timedelta

# Used by the sim to select ambulances
class DemandsCoveredAlgorithm (CoverageAlgorithm):
    """
        Barebone class. Users may subclass to implement their own algorithm for
        finding coverage.
    """

    def __init__(self):
         self.recorded_coverages: List[int] = []

    def calculateCoverage(self,
                         demands: LocationSet,
                         ambulances: List[Ambulance]):
        """
        Given a list of ambulances, find the coverage, and then append coverage.
        :param demands:
        :param ambulances:
        :return:
        """
        pass


    def avgCoverage(self):
        """

        :return: The average of the coverages so far.
        """
        return sum(self.recorded_coverages) / len(self.recorded_coverages)

    def maxCoverage(self):
        return max(self.recorded_coverages)

    def minCoverage(self):
        return min(self.recorded_coverages)

    def stdDevCoverage(self):
        std_dev = np.std(np.array([time.total_seconds() for time in l]), axis=0)
        return timedelta(std_dev.item())
