from ems.analysis.coverage.coverage import CoverageAlgorithm
from ems.datasets.travel_times.travel_times import TravelTimes


# Computes a radius coverage
class RadiusCoverage(CoverageAlgorithm):

    def __init__(self,
                 travel_times: TravelTimes,
                 percent: float = 85):
        self.travel_times = travel_times
        self.percent = percent
