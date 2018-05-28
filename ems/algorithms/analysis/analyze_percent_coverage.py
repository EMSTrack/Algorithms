
from typing import List

from ems.algorithms.analysis.coverage import CoverageAlgorithm
from ems.data.travel_times import TravelTimes
from ems.models.ambulance import Ambulance
from ems.algorithms.analysis.percent_coverage import PercentCoverage

from statistics import mean, median, mode, pstdev, pvariance

# Computes a percent coverage given a radius


class AnalyzePercentCoverage(PercentCoverage):


    def __init__(self,
                 travel_times: TravelTimes,
                 r1: int = 600
                 ):
        self._accumulate_coverage = []
        super().__init__(travel_times=travel_times, r1=r1)


    def calculate(self, ambulances: List[Ambulance]):
        """

        :param ambulances:
        :return:
        """

        result = super().calculate(ambulances)
        self._accumulate_coverage.append(result)

        return result

    def stats(self):
        data = self._accumulate_coverage

        results = {
            'mean'      : mean(data),
            'median'    : median(data),
            'mode'      : mode(data),
            'pstdev'    : pstdev(data),
            'pvariance' : pvariance(data),
        }

        return results




