# Runs the simulation.

from typing import List

from ems.algorithms.selection.ambulance_selection import AmbulanceSelectionAlgorithm
from ems.datasets.case.case_set import CaseSet
from ems.models.ambulance import Ambulance


class Simulator:

    def __init__(self,
                 ambulances: List[Ambulance],
                 case_set: CaseSet,
                 ambulance_selector: AmbulanceSelectionAlgorithm):
        self.ambulances = ambulances
        self.case_set = case_set
        self.ambulance_selector = ambulance_selector

    def run(self):
        raise NotImplementedError()
