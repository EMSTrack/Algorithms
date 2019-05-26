from datetime import datetime
from typing import List

from ems.datasets.travel_times.travel_times import TravelTimes
from ems.models.ambulances.ambulance import Ambulance
from ems.models.cases.case import Case
from ems.algorithms.selection.ambulance_selection import AmbulanceSelector
from ems.analysis.metrics.coverage.percent_coverage import PercentCoverage

from itertools import combinations


# An implementation of a "fastest travel time" ambulance_selection from a base 
# to the demand point closest to a case
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
        Runs *both* of the ambulance selection policy algorithms and then runs a weight algorithm
        to scale between the two algorithms.
        """

        if not case.priority:
            case.priority = 3
            print("WARNING: Case priority was not found but optimal dispatching requires it. ")

        # Optimization: if priority is 1, send fastest ambulance. If it's 4, send best coverage.
        loc_set_2 = self.travel_times.destinations
        closest_loc_to_case, _, _ = loc_set_2.closest(case.incident_location)

        times = self.sort_ambulances_by_traveltime(available_ambulances, closest_loc_to_case)
        coverages = self.sort_ambulances_by_coverage(available_ambulances)

        # As times increase, it is less favorable than the fastest time. For example, 
        # if t0 = 9 minutes and t1 = 10 minutes, then t1 is 9/10 or 90% favorable. 
        # t0 is always favorable because t0/t0 = 100%. 

        times = [(t[0].total_seconds(), t[1]) for t in times] 
        times = [(t[0]/times[0][0], t[1]) for t in times]

        # Do the same thing with coverage. Divide each worse coverage by the best coverage 
        # to get a < 100% score.

        # TODO

        # We are only concerned about combining the same ambulance's travel time and coverage. 
        # It is not useful to weigh together different ambulance's rankings. Hence the condition.
        priorities_applied = [(self.weighted_metrics2(t[0], c[0], case.priority), t[1]) \
        for t in times for c in coverages if t[1] == c[1]]

        priorities_applied.sort(key=lambda t: t[0])
        priorities_applied.reverse()

        # print("Chosen ambulance: ", priorities_applied[0])
        # print()

        # import IPython; IPython.embed()

        return priorities_applied[0][1]


    # This is Version 2 to weigh the two algorithms
    def weighted_metrics2(self, time, coverage, priority):
        """ Weighted dispatch as ambulance selection policy, version 2. """

        # Amplifiers for each of the weights
        alpha = 5
        beta = 1

        # Calculate each term
        t = alpha * time * abs(4 - priority)/3
        c = beta * coverage * abs(1 - priority)/3

        score = t + c
        # print("Priority: ", priority)
        # print("[{}], [{}]. ".format(time, coverage))
        # print("[{}], [{}], [{}].".format(t, c, score))
        # print()

        return score 


    # These help define the tensions between the two sorting algorithms.
    # def weighted_metrics(self, time, coverage, priority):
    #     more_weight = 4 # 3 showed improvement. 6 sucked.
    #     return time.total_seconds() * self.favor(1, priority) / (more_weight * coverage * self.favor(4, priority) + 0.000001)


    # def favor(self, priority, actual_priority):
    #     """ Compute a new metric in that aims to """
    #     return (3 - abs(priority - actual_priority))/3 + 0.000001


    # These should be the same sorting algorithms as the previous two.
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

        # Sort by the travel time.
        list_of_ambulances.sort(key=lambda t: t[0])
        list_of_ambulances.reverse()
        return list_of_ambulances



    # TODO CHANGE THIS TO SORT BY LEAST DISRUPTION
    def sort_ambulances_by_coverage(self, ambulances):
        """ Calculate all combinations of ambulances's coverage and return the best one. """
        
        potential_ambulances = list(combinations(ambulances, len(ambulances) - 1))
        list_of_ambulances = []

        for ambulance_set in potential_ambulances:
            coverage = self.coverage.calculate(datetime.now(), ambulances=ambulance_set)
            list_of_ambulances.append(
                (coverage, [a for a in ambulances if a not in ambulance_set][0])
            )

        list_of_ambulances.sort(key=lambda t: t[0])
        list_of_ambulances.reverse()
        return list_of_ambulances


