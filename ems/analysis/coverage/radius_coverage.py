from typing import List

from ems.analysis.metric import Metric
from ems.datasets.travel_times.travel_times import TravelTimes

from ems.models.ambulance import Ambulance


# Computes a radius coverage
class RadiusCoverage(Metric):

    def __init__(self,
                 travel_times: TravelTimes,
                 percent: float = 85,
                 tag = "radius_coverage"):
        super().__init__(tag)
        self.travel_times = travel_times
        self.percent = percent

    def calculate(self, ambulances: List[Ambulance]):
        pass
