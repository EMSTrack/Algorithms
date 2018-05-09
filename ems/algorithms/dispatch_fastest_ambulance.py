# The following functions define default algorithms for the DispatchAlgorithm class.
from datetime import datetime
from datetime import timedelta
from typing import List

from ems.algorithms.ambulance_selection import AmbulanceSelectionAlgorithm
from ems.data.traveltimes import TravelTimes
from ems.models.ambulance import Ambulance
from ems.models.case import Case

# An implementation of a "fastest travel time" ambulance_selection from a base to
# the demand point closest to a case


class BestTravelTimeAlgorithm(AmbulanceSelectionAlgorithm):

    def __init__(self,
                 travel_times: TravelTimes = None):
        self.travel_times = travel_times

    def select_ambulance(self,
                         available_ambulances: List[Ambulance],
                         case: Case,
                         current_time: datetime):

        # Compute the closest demand point to the case location
        closest_demand = self.travel_times.find_nearest_demand(case.location)

        # Select an ambulance to attend to the given case and obtain the its duration of travel
        chosen_ambulance, ambulance_travel_time = self.find_fastest_ambulance(
            available_ambulances, self.travel_times, closest_demand)

        # Determine the overall coverage, and each ambulance's disruption to the cost. TODO 
        # current_coverage = self.determine_coverage(ambulances, case)

        return {'choice': chosen_ambulance,
                'travel_time': ambulance_travel_time}

    def find_fastest_ambulance(self, ambulances, travel_times, demand):
        """
        Finds the ambulance with the shortest one way travel time from its base to the
        demand point
        :param ambulances:
        :param travel_times:
        :param demand:
        :return: The ambulance and the travel time
        """

        shortest_time = timedelta(hours=9999999)
        fastest_amb = None

        for amb in ambulances:
            time = travel_times.get_time(amb.base, demand)
            if shortest_time > time:
                shortest_time = time
                fastest_amb = amb

        if fastest_amb is not None:
            return fastest_amb, shortest_time

        return None, None
