# Framework for using algorithms and allowing for replacement
from typing import List

from ems.algorithms.analysis.coverage import CoverageAlgorithm
from ems.data.travel_times import TravelTimes
from ems.models.ambulance import Ambulance


# Computes a percent coverage given a radius


class PercentCoverage(CoverageAlgorithm):

    def __init__(self,
                 travel_times: TravelTimes,
                 r1: int = 600):
        self.travel_times = travel_times
        self.r1 = r1

    def mark_coverage(self, ambulances: List[Ambulance]):
        """

        :param ambulances:
        :return:
        """
        ambulance_locations = list([amb.location for amb in ambulances if not amb.deployed])
        locations_to_cover = self.travel_times.loc_set_2.locations
        locations_covered = [0 for _ in locations_to_cover]

        for index, location_to_cover in enumerate(locations_to_cover):

            for amb_location in ambulance_locations:

                # Compute closest location in location set 1 to the ambulance location
                closest_loc_to_ambulance = self.travel_times.loc_set_1.closest(amb_location)[0]

                # See if travel time is within the r1 radius and mark the location as covered if it is
                if self.travel_times.get_time(closest_loc_to_ambulance, location_to_cover).total_seconds() < self.r1:
                    locations_covered[index] += 1
                    break

        return locations_covered


    def calculate(self, ambulances: List[Ambulance]):
        """
        At a time, given a list of ambulances, determine the proportion of demands covered
        by the ambulances that are inactive

        :param ambulances:
        :return:
        """

        locations_covered = self.mark_coverage(ambulances)


        # Count how many locations are covered
        total = sum([1 for loc in locations_covered if loc > 0])

        # Return proportion of covered locations
        return total / len(locations_covered)


