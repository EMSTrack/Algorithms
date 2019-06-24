from datetime import datetime
from datetime import timedelta
from typing import List

from ems.algorithms.selection.ambulance_selection import AmbulanceSelector
from ems.datasets.travel_times.travel_times import TravelTimes
from ems.models.ambulances.ambulance import Ambulance
from ems.models.cases.case import Case
from ems.analysis.metrics.coverage.double_coverage import PercentDoubleCoverage
from ems.algorithms.selection.dispatch_fastest import BestTravelTime

from itertools import combinations

# An implementation of a "fastest travel time" ambulance_selection from a base to
# the demand point closest to a case
class LeastDisruption(BestTravelTime):

    def __init__(self,
                 travel_times: TravelTimes = None,
                 demands = None,
                 r1 = 600,
                 r2 = 840, 
                 ):
        self.travel_times = travel_times
        # self.coverage = PercentCoverage(
            # demands=demands,
            # travel_times=self.travel_times,
            # r1=r1
        # )
        self.coverage = PercentDoubleCoverage(
            demands=demands, 
            travel_times=self.travel_times,
            r1=r1, 
            r2=r2,
            )
        super().__init__(travel_times=travel_times)

    def select_ambulance(self,
                         available_ambulances: List[Ambulance],
                         case: Case,
                         current_time: datetime):

        case_priority = case.priority

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



        chosen_ambulance_set = []
        current_primary = -1
        current_secondary = -1

        potential_ambulances = list(combinations(ambulances, len(ambulances) - 1))

        # Primary coverage considered first. In the event of a tie, update the seconday coverage.
        for ambulance_set in potential_ambulances:
            primary, secondary = self.coverage.calculate(datetime.now(), ambulances=ambulance_set)
            
            # If the primary is larger, this clearly wins. 
            if primary > current_primary:
                current_primary = primary 
                current_secondary = secondary

                chosen_ambulance_set = ambulance_set


            # If the primaries are the same, then consider the larger of the secondaries.
            elif primary == current_primary: 
                if secondary > current_secondary:
                    current_secondary = secondary 
                    # TODO A future implementation of this would simply use a list and recursion. 
                    chosen_ambulance_set = ambulance_set 




        chosen_ambulance = [ambulance for ambulance in ambulances if ambulance not in chosen_ambulance_set][0]

        return chosen_ambulance, None

