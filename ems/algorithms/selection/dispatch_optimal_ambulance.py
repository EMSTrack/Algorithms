# The following functions define default algorithms for the DispatchAlgorithm class.
from datetime import datetime
from datetime import timedelta
from typing import List

from ems.algorithms.selection.ambulance_selection import AmbulanceSelectionAlgorithm
from ems.data.travel_times import TravelTimes
from ems.models.ambulance import Ambulance
from ems.models.case import Case
from ems.algorithms.selection.dispatch_fastest_ambulance import BestTravelTimeAlgorithm
from ems.algorithms.coverage.percent_coverage import PercentCoverage


# An implementation of a "fastest travel time" ambulance_selection from a base to
# the demand point closest to a case


class OptimalTravelTimeWithCoverageAlgorithm(BestTravelTimeAlgorithm):

    def __init__(self,
                 travel_times: TravelTimes = None):
        super().__init__(travel_times=travel_times)

        # This instance is used for calculating future coverages
        self.coverage = PercentCoverage(travel_times)

    def select_ambulance(self,
                         available_ambulances: List[Ambulance],
                         case: Case,
                         current_time: datetime):

        # Used for determining priorities for selecting an ambulance to maximize kept coverage or
        # minimize case duration
        case_priority = case.priority

        # TODO --
        if case_priority is None:
            # Find ambulance that when dispatched, impacts coverage the least
            pass
        else:
            # Select based on best travel time
            super().select_ambulance(available_ambulances=available_ambulances,
                                     case=case,
                                     current_time=current_time)

    def find_least_coverage_impact_ambulance(self, ambulances: List[Ambulance]):
        for i in range(len(ambulances)):
            ambulances_remaining = ambulances[:i] + ambulances[i:]
            print(ambulances_remaining)

    def determine_coverage(self):
        """

        :return:
        """
        pass


    def _rank_ambulances_speed(self):
        """
        Returns the rankings of the ambulances according to shortest to longest travel time
        :return:
        """
        pass

    def _rank_ambulances_coverage(self):
        """
        Returns the rankings of the ambulances according to the least disruption to the worst disruption.
        :return:
        """
        pass

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
