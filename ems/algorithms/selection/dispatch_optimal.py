from datetime import datetime
from typing import List
from datetime import timedelta

from ems.datasets.travel_times.travel_times import TravelTimes
from ems.models.ambulances.ambulance import Ambulance
from ems.models.cases.case import Case
from ems.algorithms.selection.dispatch_fastest import BestTravelTime
from ems.algorithms.selection.dispatch_least_cost import LeastDisruption
from ems.analysis.metrics.coverage.percent_coverage import PercentCoverage

from itertools import combinations

# An implementation of a "fastest travel time" ambulance_selection from a base to
# the demand point closest to a cas
class OptimalTravelTimeWithCoverage(BestTravelTime, LeastDisruption):

    def __init__(self,
                 travel_times: TravelTimes = None):
        super().__init__(travel_times=travel_times)

        # This instance is used for calculating future coverages
        self.coverage = PercentCoverage(travel_times)

    def select_ambulance(self,
                         available_ambulances: List[Ambulance],
                         case: Case,
                         current_time: datetime):
        # This function must override the two possibly conflicting inherited method of the same name.
        # Used for determining priorities for selecting an ambulance to maximize kept coverage or
        # minimize case duration
        case_priority = case.priority

        # TODO
        if case_priority is None:
            # Find ambulance that when dispatched, impacts coverage the least
            pass
        else:
            # Select based on best travel time
            super().select_ambulance(available_ambulances=available_ambulances,
                                     case=case,
                                     current_time=current_time)

    # TODO CHANGE THIS METHOD TO SORT BY FASTEST AMBULANCE
    def find_fastest_ambulance(self, ambulances, closest_loc_to_case):
        """
        Finds the ambulance with the shortest one way travel time from its base to the
        demand point
        :param ambulances:
        :param closest_loc_to_case:
        :return: The ambulance and the travel time
        """

        shortest_time = timedelta.max
        fastest_amb = None

        loc_set_1 = self.travel_times.origins

        for amb in ambulances:

            # Compute closest location in the first set to the ambulance
            ambulance_location = amb.location

            # Compute closest location in location set 1 to the ambulance location
            closest_loc_to_ambulance = loc_set_1.closest(ambulance_location)[0]

            # Compute the time from the location point mapped to the ambulance to the location point mapped to the case
            time = self.travel_times.get_time(closest_loc_to_ambulance, closest_loc_to_case)
            if shortest_time > time:
                shortest_time = time
                fastest_amb = amb

        if fastest_amb is not None:
            return fastest_amb, shortest_time

        return None, None


    # TODO CHANGE THIS TO SORT BY LEAST DISRUPTION
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
        current_coverage = -1

        potential_ambulances = combinations(ambulances, len(ambulances) - 1)

        for ambulance_set in potential_ambulances:
            coverage = self.coverage.calculate(datetime.now(), ambulances=ambulance_set)
            if coverage > current_coverage:
                current_coverage = coverage
                chosen_ambulance_set = ambulance_set

        chosen_ambulance = [ambulance for ambulance in ambulances if ambulance not in chosen_ambulance_set][0]

        return chosen_ambulance, None






    # def find_least_coverage_impact_ambulance(self, ambulances: List[Ambulance]):
    #     for i in range(len(ambulances)):
    #         ambulances_remaining = ambulances[:i] + ambulances[i:]
    #         print(ambulances_remaining)
    #
    # def determine_coverage(self):
    #     """
    #
    #     :return:
    #     """
    #     pass
    #
    #
    # def _rank_ambulances_speed(self):
    #     """
    #     Returns the rankings of the ambulances according to shortest to longest travel time
    #     :return:
    #     """
    #     pass
    #
    # def _rank_ambulances_coverage(self):
    #     """
    #     Returns the rankings of the ambulances according to the least disruption to the worst disruption.
    #     :return:
    #     """
    #     pass

    # def select_ambulance(self,
    #                      available_ambulances: List[Ambulance],
    #                      case: Case,
    #                      current_time: datetime):
    #
    #     # Compute the closest demand point to the case location
    #     demands = self.base_demand_travel_times.loc_set_2
    #     closest_demand, distance = demands.closest(case.location)
    #
    #     # Select an ambulance to attend to the given case and obtain the its duration of travel
    #     chosen_ambulance, ambulance_travel_time = self.find_fastest_ambulance(
    #         available_ambulances, self.base_demand_travel_times, closest_demand)
    #
    #     return {'choice': chosen_ambulance,
    #             'travel_time': ambulance_travel_time}

    # def find_fastest_ambulance(self, ambulances, travel_times, demand):
    #     """
    #     Finds the ambulance with the shortest one way travel time from its base to the
    #     demand point
    #     :param ambulances:
    #     :param travel_times:
    #     :param demand:
    #     :return: The ambulance and the travel time
    #     """
    #
    #     shortest_time = timedelta(hours=9999999)
    #     fastest_amb = None
    #
    #     for amb in ambulances:
    #         time = travel_times.get_time(amb.base, demand)
    #         if shortest_time > time:
    #             shortest_time = time
    #             fastest_amb = amb
    #
    #     if fastest_amb is not None:
    #         return fastest_amb, shortest_time
    #
    #     return None, None
