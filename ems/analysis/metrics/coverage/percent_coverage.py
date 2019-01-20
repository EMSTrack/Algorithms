# Framework for using algorithms and allowing for replacement
from datetime import timedelta, datetime

from ems.analysis.metrics.metric import Metric
from ems.datasets.location.location_set import LocationSet
from ems.datasets.travel_times.travel_times import TravelTimes


# Computes a percent coverage given a radius


class PercentCoverage(Metric):

    def __init__(self,
                 demands: LocationSet,
                 travel_times: TravelTimes,
                 r1: timedelta = timedelta(600),
                 tag = 'percent_coverage'):
        super().__init__(tag=tag)
        self.demands = demands
        self.travel_times = travel_times
        self.r1 = r1

        # Caching for better performance
        self.coverage_state = PercentCoverageState(ambulances=set(),
                                                   locations_coverage=[set() for _ in demands.locations])

    def calculate(self,
                  timestamp: datetime,
                  **kwargs):

        if "ambulances" not in kwargs:
            return None

        ambulances = kwargs["ambulances"]

        available_ambulances = [amb for amb in ambulances if not amb.deployed]

        ambulances_to_add = [a for a in available_ambulances if a not in self.coverage_state.ambulances]
        ambulances_to_remove = [a for a in self.coverage_state.ambulances if a not in available_ambulances]

        for ambulance in ambulances_to_add:
            self.add_ambulance_coverage(ambulance)

        for ambulance in ambulances_to_remove:
            self.remove_ambulance_coverage(ambulance)

        sm = 0
        for location_coverage in self.coverage_state.locations_coverage:
            if len(location_coverage) > 0:
                sm += 1

        return sm/len(self.demands)

    def add_ambulance_coverage(self, ambulance):

        # Retrieve closest point from set 1 to the ambulance
        closest_to_amb, _, _ = self.travel_times.origins.closest(ambulance.location)

        for index, demand_loc in enumerate(self.demands.locations):

            # Retrieve closest point from set 2 to the demand
            closest_to_demand, _, _ = self.travel_times.destinations.closest(demand_loc)

            # Compute time and determine if less than r1
            if self.travel_times.get_time(closest_to_amb, closest_to_demand) <= self.r1:
                self.coverage_state.locations_coverage[index].add(ambulance)

        # Register ambulance as covering some area
        self.coverage_state.ambulances.add(ambulance)

    def remove_ambulance_coverage(self, ambulance):

        for location_coverage in self.coverage_state.locations_coverage:

            # Remove ambulance from covering the location
            if ambulance in location_coverage:
                location_coverage.remove(ambulance)

        # Unregister ambulance as covering some area
        self.coverage_state.ambulances.remove(ambulance)


class PercentCoverageState:

    def __init__(self,
                 ambulances,
                 locations_coverage):
        self.ambulances = ambulances
        self.locations_coverage = locations_coverage

