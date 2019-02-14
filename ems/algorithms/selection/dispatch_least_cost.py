from datetime import datetime
from datetime import timedelta
from typing import List

from ems.algorithms.selection.ambulance_selection import AmbulanceSelector
from ems.datasets.travel_times.travel_times import TravelTimes
from ems.models.ambulances.ambulance import Ambulance
from ems.models.cases.case import Case
from ems.analysis.metrics.coverage.percent_coverage import PercentCoverage

# An implementation of a "fastest travel time" ambulance_selection from a base to
# the demand point closest to a case
class LeastDisruption(AmbulanceSelector):

    def __init__(self,
                 travel_times: TravelTimes = None,
                 demands = None,
                 r1 = 600,
                 ):
        self.travel_times = travel_times
        self.coverage = PercentCoverage(
            demands=demands,
            travel_times=self.travel_times,
            r1=r1
        )

    def select_ambulance(self,
                         available_ambulances: List[Ambulance],
                         case: Case,
                         current_time: datetime):

        case_priority = case.priority


        # Compute the closest demand point to the case location
        # loc_set_2 = self.travel_times.destinations
        # closest_loc_to_case, _, _ = loc_set_2.closest(case.incident_location)

        # Select an ambulance that disrupts the coverage the least regardless of travel time.
        chosen_ambulance, ambulance_travel_time = self.find_least_disruption(available_ambulances)
        return chosen_ambulance


    def find_least_disruption(self, ambulances):
        """
        Finds the ambulance with the shortest one way travel time from its base to the
        demand point
        :param ambulances:
        :param closest_loc_to_case:
        :return: The ambulance and the travel time
        """

        # Calculate all combinations of ambulances's coverage and return the best one.
        from itertools import combinations


        chosen_ambulance_set = []
        current_coverage = -1

        potential_ambulances = combinations(ambulances, len(ambulances) - 1)

        for ambulance_set in potential_ambulances:
            coverage = self.coverage.calculate(datetime.now(), ambulances=ambulance_set)
            if coverage > current_coverage:
                current_coverage = coverage
                chosen_ambulance_set = ambulance_set

        chosen_ambulance = [ambulance for ambulance in ambulances if ambulance not in chosen_ambulance_set][0]

        # from IPython import embed;
        # embed()
            # for ambulance in ambulance_set:
            #     self.coverage._remove_ambulance_coverage(ambulance)


        return chosen_ambulance, None

