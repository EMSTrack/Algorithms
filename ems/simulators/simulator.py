# Runs the simulation.

from typing import List

from ems.algorithms.selection.ambulance_selection import AmbulanceSelector

from ems.analysis.metrics.metric_aggregator import MetricAggregator
from ems.datasets.ambulance.ambulance_set import AmbulanceSet
from ems.datasets.case.case_set import CaseSet


class Simulator:

    def __init__(self,
                 ambulances: AmbulanceSet,
                 cases: CaseSet,
                 ambulance_selector: AmbulanceSelector,
                 metric_aggregator: MetricAggregator,
                 debug:bool = False):

        self.ambulances = ambulances
        self.cases = cases
        self.ambulance_selector = ambulance_selector
        self.metric_aggregator = metric_aggregator
        self.debug = debug

    def run(self):
        raise NotImplementedError()
