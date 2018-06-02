
from typing import List

from ems.algorithms.coverage.coverage import CoverageAlgorithm
from ems.data.travel_times import TravelTimes
from ems.models.ambulance import Ambulance
from ems.algorithms.coverage.percent_coverage import PercentCoverage

from statistics import mean, median, mode, pstdev, pvariance

import matplotlib.pyplot as plt

# Computes a percent coverage given a radius


class AnalyzePercentCoverage(PercentCoverage):


    def __init__(self,
                 travel_times: TravelTimes,
                 r1: int = 600
                 ):
        self._accumulate_coverage = []
        super().__init__(travel_times=travel_times, r1=r1)


    def calculate(self, ambulances: List[Ambulance], plot: bool):
        """

        :param ambulances:
        :return:
        """

        locations_covered = super().mark_coverage(ambulances)
        locations = self.travel_times.loc_set_2.locations

        if plot:
            plt.scatter(
                [locations[i].longitude for i in range(len(locations)) if locations_covered[i] >= 1],
                [locations[i].latitude for i in range(len(locations)) if locations_covered[i] >= 1],
                color='green'
            )

            plt.scatter(
                [locations[i].longitude for i in range(len(locations)) if locations_covered[i] == 0],
                [locations[i].latitude for i in range(len(locations)) if locations_covered[i] == 0],
                color='red'
            )
            plt.show()

        # Count how many locations are covered
        total = sum([1 for loc in locations_covered if loc > 0])
        percentage = total / len(locations_covered)
        self._accumulate_coverage.append(percentage)

        # Return proportion of covered locations
        return percentage


    def stats(self):
        data = self._accumulate_coverage

        results = {
            'elems'     : data,
            'max'       : max(data),
            'min'       : min(data),
            'mean'      : mean(data),
            'median'    : median(data),
            'mode'      : mode(data),
            'pstdev'    : pstdev(data),
            'pvariance' : pvariance(data),
            'count'     : len(data),
        }

        return results

    def chart(self):
        plt.plot(self._accumulate_coverage)
        plt.xlabel('Case')
        plt.ylabel('Coverage in Percent')
        plt.show()


