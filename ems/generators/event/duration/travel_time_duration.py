import datetime

from geopy import Point

from ems.datasets.travel_times.travel_times import TravelTimes
from ems.generators.event.duration.duration import EventDurationGenerator
from ems.models.ambulances.ambulance import Ambulance


class TravelTimeDurationGenerator(EventDurationGenerator):

    def __init__(self,
                 travel_times: TravelTimes):
        self.travel_times = travel_times

    def generate(self,
                 ambulance: Ambulance,
                 destination: Point,
                 timestamp: datetime):
        # Compute the point from first location set to the ambulance location
        loc_set_1 = self.travel_times.origins
        closest_loc_to_orig, _, _ = loc_set_1.closest(ambulance.location)

        # Compute the point from the second location set to the destination
        loc_set_2 = self.travel_times.destinations
        closest_loc_to_dest, _, _ = loc_set_2.closest(destination)

        # Return time lookup
        return self.travel_times.get_time(closest_loc_to_orig, closest_loc_to_dest)