from datetime import datetime
from typing import List

from ems.datasets.travel_times.travel_times import TravelTimes
from ems.models.ambulances.ambulance import Ambulance
from ems.models.cases.case import Case
from ems.algorithms.selection.ambulance_selection import AmbulanceSelector
from ems.analysis.metrics.coverage.percent_coverage import PercentCoverage

from itertools import combinations

class WeightedDispatch(AmbulanceSelector):
	"""
		A weighting class between the best travel time and best coverage. Version 2.
	"""

    def __init__(self,
                 travel_times: TravelTimes = None,
                 demands=None,
                 r1=600,
                 ):