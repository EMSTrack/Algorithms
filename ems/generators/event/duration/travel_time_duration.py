import datetime

from geopy import Point
from geopy.distance import distance

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

        # Calculate the error as a percentage between the sim dist and the real dist
        sim_dist  = distance(closest_loc_to_dest, closest_loc_to_orig)
        real_dist = distance(destination, ambulance.location)
        difference = sim_dist/real_dist * 100 - 100

        # Return time lookup
        return {'duration': self.travel_times.get_time(closest_loc_to_orig, closest_loc_to_dest),
                'error'   : difference }