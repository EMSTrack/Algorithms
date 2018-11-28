from datetime import timedelta, datetime
from typing import List

from ems.analysis.metric import Metric
from ems.datasets.location.location_set import LocationSet
from ems.datasets.travel_times.travel_times import TravelTimes

from ems.models.ambulance import Ambulance


# Computes a radius coverage
from ems.models.cases.case import Case


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

        # self.coverage_state = RadiusCoverageState(ambulances=[],
        #                                           tt_to_ambulance=[None for _ in demands.locations])

    def calculate(self,
                  timestamp: datetime,
                  **kwargs):

        if "ambulances" not in kwargs:
            return None

        ambulances = kwargs["ambulances"]

        # available_ambulances = [amb for amb in ambulances if not amb.deployed]
        #
        # ambulances_to_add = [a for a in available_ambulances if a not in self.coverage_state.ambulances]
        # ambulances_to_remove = [a for a in self.coverage_state.ambulances if a not in available_ambulances]

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
        return {self.tag: max(min_tts), "timestamp": timestamp}

    # def add_ambulance_coverage(self, ambulance):
    #
    #     # Retrieve closest point from set 1 to the ambulance
    #     closest_to_amb, _, _ = self.travel_times.loc_set_1.closest(ambulance.location)
    #
    #     for index, demand_location in enumerate(self.demands.locations):
    #
    #         closest_to_dem = self.travel_times.loc_set_2.closest(demand_location)
    #
    #         tt = self.travel_times.get_time(closest_to_amb, closest_to_dem)
    #
    #         if self.coverage_state.tt_to_ambulance is None or self.coverage_state.tt_to_ambulance[index][1] > tt:
    #             self.coverage_state.tt_to_ambulance[index] = (ambulance, tt)
    #
    #     # Register ambulance as covering some area
    #     self.coverage_state.ambulances.add(ambulance)
    #
    # def remove_ambulance_coverage(self, ambulance):
    #
    #     # for location_coverage in self.coverage_state.locations_coverage:
    #     #
    #     #     # Remove ambulance from covering the location
    #     #     if ambulance in location_coverage:
    #     #         location_coverage.remove(ambulance)
    #
    #     # Unregister ambulance as covering some area
    #     self.coverage_state.ambulances.remove(ambulance)

# # Used for caching operations
# class RadiusCoverageState:
#
#     def __init__(self,
#                  ambulances,
#                  tt_to_ambulance: List):
#         self.ambulances = ambulances
#         self.tt_to_ambulance = tt_to_ambulance
