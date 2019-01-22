import numpy as np

from ems.datasets.location.kd_tree_location_set import KDTreeLocationSet
from ems.datasets.travel_times.travel_times import TravelTimes
from ems.utils import parse_unheadered_csv


class FilteredTijuanaBaseSet(KDTreeLocationSet):

    def __init__(self,
                 filename: str,
                 count: int,
                 required_travel_time: int,
                 travel_times: TravelTimes):
        self.filename = filename
        self.count = count
        self.required_travel_time = required_travel_time
        self.travel_times = travel_times
        latitudes, longitudes = self.read_bases(filename)
        super().__init__(latitudes, longitudes)

    def read_bases(self, filename):
        # Read bases from an unheadered CSV into a pandas dataframe
        base_col_positions = [4, 5]
        base_headers = ["lat", "long"]
        bases_df = parse_unheadered_csv(filename, base_col_positions, base_headers)

        # Generate list of models from dataframe
        latitudes = []
        longitudes = []
        for index, row in bases_df.iterrows():
            latitudes.append(row["lat"])
            longitudes.append(row["long"])

        latitudes, longitudes = self.kmeans_filter(latitudes, longitudes)

        return latitudes, longitudes

    def kmeans_filter(self, latitudes, longitudes):

        np_travel_times = np.array(self.travel_times.times)
        chosen_latitudes = []
        chosen_longitudes = []
        demands_covered = 0

        for _ in range(self.count):
            # Make a True/False table of the travel_times and then count how many covered.
            covered = [[t < self.required_travel_time for t in row] for row in np_travel_times]
            count_covered = [(index, covered[index].count(True)) for index in range(len(covered))]
            d = [('index', int), ('covered', int)]
            count_covered = np.array(count_covered, d)

            # Sort the table by row and grab the last element (the base with the most coverage)
            (best_base, count) = np.sort(count_covered, order='covered', kind='mergesort')[-1]
            chosen_latitudes.append(latitudes[best_base])
            chosen_longitudes.append(longitudes[best_base])
            demands_covered += count
            demand_coverage = covered[best_base]

            # Delete the covered columns
            delete_cols = [d for d in range(len(demand_coverage)) if demand_coverage[d]]
            np_travel_times = np.delete(np_travel_times, delete_cols, axis=1)

        return chosen_latitudes, chosen_longitudes
