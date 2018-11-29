import datetime

from geopy import Point

from ems.datasets.travel_times.travel_times import TravelTimes
from ems.generators.event.duration import EventDurationGenerator
from ems.models.ambulance import Ambulance


class TravelTimeDurationGenerator(EventDurationGenerator):

    def __init__(self,
                 travel_times: TravelTimes):
        self.travel_times = travel_times

    def generate(self,
                 ambulance: Ambulance,
                 destination: Point,
                 current_time: datetime):
        # Compute the point from first location set to the ambulance location
        loc_set_1 = self.travel_times.loc_set_1
        closest_loc_to_orig, _, _ = loc_set_1.closest(ambulance.location)

        # Compute the point from the second location set to the destination
        loc_set_2 = self.travel_times.loc_set_2
        closest_loc_to_dest, _, _ = loc_set_2.closest(destination)

        # Return time lookup
        print('Orig: {}'.format(str(closest_loc_to_orig))) #TODO
        print('Dest: {}'.format(str(closest_loc_to_dest))) #TODO
        return self.travel_times.get_time(closest_loc_to_orig, closest_loc_to_dest)