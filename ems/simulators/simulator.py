# Runs the simulation.

from typing import List

from ems.algorithms.selection.ambulance_selection import AmbulanceSelectionAlgorithm

from ems.analysis.metrics.metric_aggregator import MetricAggregator
from ems.datasets.ambulance.ambulance_set import AmbulanceSet
from ems.datasets.case.case_set import CaseSet
from ems.models.ambulances.ambulance import Ambulance


class Simulator:

    def __init__(self,
                 ambulance_set: AmbulanceSet,
                 case_set: CaseSet,
                 ambulance_selector: AmbulanceSelectionAlgorithm,
                 metric_aggregator: MetricAggregator):
        self.ambulance_set = ambulance_set
        self.case_set = case_set
        self.ambulance_selector = ambulance_selector
        self.metric_aggregator = metric_aggregator

    def run(self):
        raise NotImplementedError()
