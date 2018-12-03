import numpy as np

from ems.algorithms.base_selectors.selector import AmbulanceBaseSelector
from ems.datasets.location.location_set import LocationSet
from ems.datasets.travel_times.travel_times import TravelTimes


class RoundRobinBaseSelector(AmbulanceBaseSelector):

    def __init__(self,
                 base_set: LocationSet):
        self.base_set = base_set

    def select(self, num_ambulances):

        bases = []

        for index in range(num_ambulances):
            base_index = index % len(self.base_set)
            bases.append(self.base_set.locations[base_index])

        return bases
