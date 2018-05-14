# Framework for using algorithms and allowing for replacement
from typing import List

import numpy as np

from ems.algorithms.analysis.coverage import CoverageAlgorithm
from ems.data.travel_times import TravelTimes
from ems.models.ambulance import Ambulance


# Used by the sim to select ambulances
from ems.models.location import Location


class DemandCoverage(CoverageAlgorithm):

    def __init__(self,
                 travel_times: TravelTimes,
                 r1: int = 600):
        self.travel_times = travel_times
        self.r1 = r1
        # self._recorded_coverages = []

    def calculate_coverage(self, ambulances: List[Ambulance]):
        """
        At a time, given a list of ambulances, determine the analysis of all the demands.

        :param ambulances:
        :return:
        """

        ambulance_locations = list([amb.location for amb in ambulances if not amb.deployed])
        locations_to_cover = self.travel_times.loc_set_2.locations
        locations_covered = [0 for _ in locations_to_cover]

        for index, location_to_cover in enumerate(locations_to_cover):

            for amb_location in ambulance_locations:

                # Compute closest location in location set 1 to the ambulance location
                if type(amb_location) is Location:
                    amb_location = amb_location.location

                closest_loc_to_ambulance = self.travel_times.loc_set_1.closest(amb_location)[0]

                # See if travel time is within the r1 radius
                if self.travel_times.get_time(closest_loc_to_ambulance, location_to_cover).total_seconds() < self.r1:
                    locations_covered[index] += 1
                    break

        total = sum([1 for loc in locations_covered if loc > 0])

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
