from datetime import datetime

from geopy import Point

from ems.algorithms.times.duration_algorithm import DurationAlgorithm
from ems.datasets.travel_times import TravelTimes
from ems.models.ambulance import Ambulance
from ems.models.cases.case import Case


class TravelTimeLookupAlgorithm(DurationAlgorithm):

    def __init__(self, travel_times: TravelTimes):
        self.travel_times = travel_times

    def compute_duration(self,
                         ambulance: Ambulance,
                         case: Case,
                         origin: Point,
                         destination: Point,
                         current_time: datetime):
        # Compute the point from first location set to the origin
        loc_set_1 = self.travel_times.loc_set_1
        closest_loc_to_orig, _, _ = loc_set_1.closest(destination)

        # Compute the point from the second location set to the destination
        loc_set_2 = self.travel_times.loc_set_2
        closest_loc_to_dest, _, _ = loc_set_2.closest(destination)

        # Return time lookup
        return self.travel_times.get_time(closest_loc_to_orig, closest_loc_to_dest)
