from datetime import datetime
from typing import List

from ems.datasets.travel_times.travel_times import TravelTimes
from ems.models.ambulances.ambulance import Ambulance
from ems.models.cases.case import Case
from ems.algorithms.selection.ambulance_selection import AmbulanceSelector
from ems.analysis.metrics.coverage.percent_coverage import PercentCoverage

from itertools import combinations

# An implementation of a "fastest travel time" ambulance_selection from a base to
# the demand point closest to a cas
class OptimalTravelTimeWithCoverage(AmbulanceSelector):

    def __init__(self,
                 travel_times: TravelTimes = None,
                 demands=None,
                 r1=600,
                 ):

        self.travel_times = travel_times
        # This instance is used for calculating future coverages

        self.coverage = PercentCoverage(
            demands=demands,
            travel_times=self.travel_times,
            r1=r1
        )


    def select_ambulance(self,
                         available_ambulances: List[Ambulance],
                         case: Case,
                         current_time: datetime,
                         ):
        """

        :param available_ambulances:
        :param case:
        :param current_time:
        :return:
        """


        if not case.priority:
            case.priority = 3
            print("WARNING: Case priority was not found but optimal dispatching requires it. ")

        # Optimization: if priority is 1, send fastest ambulance. If it's 5, send best coverage.

        loc_set_2 = self.travel_times.destinations
        closest_loc_to_case, _, _ = loc_set_2.closest(case.incident_location)

        # if case.priority == 1:
        #     return self.sort_ambulances_by_traveltime(available_ambulances, closest_loc_to_case)[0][1]
        #
        # elif case.priority == 5:
        #     return self.sort_ambulances_by_coverage(available_ambulances)[0][1]
        #
        # else:

        times = self.sort_ambulances_by_traveltime(available_ambulances, closest_loc_to_case)
        coverages  = self.sort_ambulances_by_coverage(available_ambulances)

        priorities_applied = [(
            self.weighted_metrics(t[0], c[0], case.priority),
            t[1])
            for t in times for c in coverages if t[1] == c[1]]

        # from IPython import embed; embed()

        # lists = times,coverages,priorities_applied
        # for l in lists:
        #     l.sort(key=lambda t: t[0])

        # from pprint import PrettyPrinter
        # pprint = PrettyPrinter(indent=2).pprint
        # print("Case priority: {}".format(case.priority))
        # pprint(times)
        # pprint(coverages)
        # pprint(priorities_applied)
        # TODO, NOW SELECT THE AMBULANCE BASED ON THE SEVERITY

        priorities_applied.sort(key=lambda t: t[0])
        return priorities_applied[0][1]


        # Select based on best travel time
        # super().select_ambulance(available_ambulances=available_ambulances,
        #                              case=case,
        #                              current_time=current_time)


    def weighted_metrics(self, time, coverage, priority):
        return time.total_seconds() * self.favor(1, priority) / (coverage * self.favor(4, priority) + 0.000001)

    def favor(self, priority, actual_priority):
        """ Compute a new metric in that aims to """
        return (3 - abs(priority - actual_priority))/3 + 0.000001


    def sort_ambulances_by_traveltime(self, ambulances, closest_loc_to_case):
        """
        Finds the ambulance with the shortest one way travel time from its base to the
        demand point
        :param ambulances:
        :param closest_loc_to_case:
        :return: The ambulance and the travel time
        """

        loc_set_1 = self.travel_times.origins

        list_of_ambulances = []

        for amb in ambulances:

            # Compute closest location in the first set to the ambulance
            ambulance_location = amb.location

            # Compute closest location in location set 1 to the ambulance location
            closest_loc_to_ambulance = loc_set_1.closest(ambulance_location)[0]

            # Compute the time from the location point mapped to the ambulance to the location point mapped to the case
            time = self.travel_times.get_time(closest_loc_to_ambulance, closest_loc_to_case)

            list_of_ambulances.append(
                (time, amb)
            )
            # if shortest_time > time:
            #     shortest_time = time
            #     fastest_amb = amb

        # if fastest_amb is not None:
        #     return fastest_amb, shortest_time
        # list_of_ambulances.sort(key=lambda t: t[0])
        return list_of_ambulances
        # return None, None


    # TODO CHANGE THIS TO SORT BY LEAST DISRUPTION
    def sort_ambulances_by_coverage(self, ambulances):
        """

        :param ambulances:
        :return:
        """

        # Calculate all combinations of ambulances's coverage and return the best one.


        potential_ambulances = list(combinations(ambulances, len(ambulances) - 1))

        list_of_ambulances = []

        for ambulance_set in potential_ambulances:
            coverage = self.coverage.calculate(datetime.now(), ambulances=ambulance_set)
            list_of_ambulances.append(
                (coverage, [a for a in ambulances if a not in ambulance_set][0])
            )
        # list_of_ambulances.sort(key=lambda t: t[0])
        return list_of_ambulances
