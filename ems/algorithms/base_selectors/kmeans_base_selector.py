import numpy as np

from ems.algorithms.base_selectors.amb_base_selector import AmbulanceBaseSelector
from ems.datasets.location.location_set import LocationSet
from ems.datasets.travel_times.travel_times import TravelTimes


class KMeansBaseSelector(AmbulanceBaseSelector):

    def __init__(self,
                 base_set: LocationSet,
                 travel_times: TravelTimes,
                 num_bases: int,
                 required_travel_time: int=600):
        self.base_set = base_set
        self.travel_times = travel_times
        self.num_bases = num_bases
        self.required_travel_time = required_travel_time
        self.base_locations = self.pick_starting_bases()

    def pick_starting_bases(self):
        np_travel_times = np.array(self.travel_times.times)
        chosen_bases = []
        demands_covered = 0

        for _ in range(self.num_bases):
            # Make a True/False table of the travel_times and then count how many covered.
            covered = [[t < self.required_travel_time for t in row] for row in np_travel_times]
            count_covered = [(index, covered[index].count(True)) for index in range(len(covered))]
            d = [('index', int), ('covered', int)]
            count_covered = np.array(count_covered, d)

            # Sort the table by row and grab the last element (the base with the most coverage)
            (best_base, count) = np.sort(count_covered, order='covered', kind='mergesort')[-1]
            chosen_bases.append(self.base_set.locations[best_base])
            demands_covered += count
            demand_coverage = covered[best_base]

            # Delete the covered columns
            delete_cols = [d for d in range(len(demand_coverage)) if demand_coverage[d]]
            np_travel_times = np.delete(np_travel_times, delete_cols, axis=1)

        return chosen_bases

    def select(self, num_ambulances):

        bases = []

        for index in range(num_ambulances):
            base_index = index % self.num_bases
            bases.append(self.base_locations[base_index])

        return bases
