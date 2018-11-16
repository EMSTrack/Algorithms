from datetime import timedelta
from typing import List

from ems.analysis.metric import Metric
from ems.datasets.location.location_set import LocationSet
from ems.datasets.travel_times.travel_times import TravelTimes

from ems.models.ambulance import Ambulance


# Computes a radius coverage
class RadiusCoverage(Metric):

    def __init__(self,
                 demands: LocationSet,
                 travel_times: TravelTimes,
                 percent: float = 85,
                 tag="radius_coverage"):
        super().__init__(tag)
        self.demands = demands
        self.travel_times = travel_times
        self.percent = percent

    def calculate(self, ambulances: List[Ambulance]):
        # Snap ambulance location to closest location in loc_set_1
        ambulance_locations = [self.travel_times.loc_set_1.closest(ambulance.location)[0] for ambulance in ambulances if
                               not ambulance.deployed]

        if len(ambulance_locations) == 0:
            return timedelta.max

        # Snap demand location to closest location in loc_set_2
        demand_locations = [self.travel_times.loc_set_2.closest(demand_location)[0] for demand_location in
                            self.demands.locations]

        min_tts = []

        # Find the travel time from each demand to the closest ambulance (aka minimum travel time)
        for demand_location in demand_locations:
            tt_to_ambulance = [self.travel_times.get_time(ambulance_location, demand_location) for ambulance_location in
                               ambulance_locations]
            min_tts.append(min(tt_to_ambulance))

        # Take the max of those travel times
        return max(min_tts)

# TODO -- caching operations!
# class RadiusCoverageState:
#
#     def __init__(self,
#                  ambulances,
#                  tt_to_ambulance: List[]):
