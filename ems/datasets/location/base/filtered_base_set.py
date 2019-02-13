from typing import List

import numpy as np

from ems.datasets.location.kd_tree_location_set import KDTreeLocationSet
from ems.datasets.travel_times.travel_times import TravelTimes
from ems.utils import parse_headered_csv
from multiprocessing import Pool
from multiprocessing import cpu_count


class FilteredBaseSet(KDTreeLocationSet):

    def __init__(self,
                 count: int,
                 r1: int,
                 r2: int,
                 travel_times: TravelTimes,
                 filename: str = None,
                 latitudes: List[float] = None,
                 longitudes: List[float] = None,
                 debug: bool = False,
                 ):
        self.filename = filename
        self.count = count
        self.r1 = r1
        self.r2 = r2
        self.travel_times = travel_times
        self.debug = debug

        if filename is not None:
            latitudes, longitudes = self.read_bases(filename)

        latitudes, longitudes = self.kmeans_filter(latitudes, longitudes)
        super().__init__(latitudes, longitudes)

    def read_bases(self, filename):
        # Read bases from a headered CSV into a pandas dataframe
        base_headers = ["latitude", "longitude"]
        bases_df = parse_headered_csv(filename, base_headers)

        # Generate list of models from dataframe
        latitudes = []
        longitudes = []
        for index, row in bases_df.iterrows():
            latitudes.append(row["latitude"])
            longitudes.append(row["longitude"])

        return latitudes, longitudes

    def kmeans_filter(self, latitudes, longitudes):

        self.latitudes = latitudes
        self.longitudes = longitudes

        indices = [i for i in range(len(latitudes) - 1)]
        indices = indices[0: len(indices) ]
        print("Number of different combinations: ", len(indices))
        self.indices_count = len(indices)


        with Pool(cpu_count()- 1) as p:
            bases_and_coverages = p.map(self.kmeans_filter_i, indices)


        # Sort by primary coverage, secondary coverage. Return the lats and lons.
        bases_and_coverages.sort()
        bases_and_coverages = bases_and_coverages[-1]

        print("Primary and Secondary coverages: {}, {}".format(bases_and_coverages[0], bases_and_coverages[1]))

        # TODO when consistent, this won't be necessary anymore
        with open("./results/initial_coverage.txt", 'w') as fi:
            fi.write("{}, {}".format(bases_and_coverages[0], bases_and_coverages[1]))

        return bases_and_coverages[2], bases_and_coverages[3]


    def kmeans_filter_i(self, i):

        if i < self.indices_count and self.debug:
            print("{} \tout of {} ".format(i, self.indices_count))

        # i = 0

        np_travel_times = np.array(self.travel_times.times)
        chosen_latitudes = []
        chosen_longitudes = []
        primary_demands_covered = 0
        chosen_bases = []


        first_time = True

        for _ in range(self.count):

            if not first_time: i = 0

            # Make a True/False table of the travel_times and then count how many covered.
            primary_covered = [[t < self.r1 for t in row] for row in np_travel_times]
            # secondary_count = [[t < self.r2 for t in row] for row in np_travel_times]
            count_covered = [(index,
                              primary_covered[index].count(True),
                              # secondary_count[index].count(True)
                              ) for index in range(len(primary_covered))
                             ]
            d = [('index', int), ('covered', int)]
            count_covered = np.array(count_covered, d)

            # Sort the table by row and grab the last element (the base with the most coverage)
            (best_base, primary_count) = \
                np.sort(count_covered, order='covered', kind='mergesort')[-1 - i]

            first_time = False
            chosen_latitudes.append(self.latitudes[best_base])
            chosen_longitudes.append(self.longitudes[best_base])
            primary_demands_covered += primary_count
            demand_coverage = primary_covered[best_base]

            chosen_bases.append(best_base)


            # Delete the covered columns
            delete_cols = [d for d in range(len(demand_coverage)) if demand_coverage[d]]
            np_travel_times = np.delete(np_travel_times, delete_cols, axis=1)


        # Make another copy of the travel times with only the rows of the best bases
        # Really, we should be using the metric version but it seems to not really fit in with this part.
        secondary_demands_covered = 0
        new_matrix = [self.travel_times.times[i] for i in range(len(self.travel_times.times)) if i in chosen_bases]

        for demand_id in range(len(new_matrix[0])):
            # Determine if there is a primary coverage and a secondary coverage < r2
            primary = None

            # I want the minimum primary time. If there are more than one, then secondary coverage is true if
            # it has more elements that this.
            primaries = [base_times[demand_id] for base_times in new_matrix \
                                   if base_times[demand_id] <= self.r1]

            # for base_times in new_matrix:
            #     if base_times[demand_id] < self.r1:
            #         primary = base_times[demand_id]

            if not primaries:
                continue

            secondaries = [base_times[demand_id] for base_times in new_matrix if
                           base_times[demand_id] <= self.r2]


            if [min(primaries)] != secondaries:
                secondary_demands_covered += 1


        # print(primary_demands_covered, secondary_demands_covered, primary_demands_covered - secondary_demands_covered)

        if primary_demands_covered < secondary_demands_covered:
            raise Exception("The secondary coverage should always be <= primary coverage.")

        return primary_demands_covered, secondary_demands_covered, chosen_latitudes, chosen_longitudes
        # return chosen_latitudes, chosen_longitudes

