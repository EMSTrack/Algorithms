# Runs the simulation.

from typing import List

from ems.algorithms.selection.ambulance_selection import AmbulanceSelectionAlgorithm
from ems.models.ambulance import Ambulance
from ems.models.case import AbstractCase


class Simulator:

    def __init__(self,
                 ambulances: List[Ambulance],
                 cases: List[AbstractCase],
                 ambulance_selector: AmbulanceSelectionAlgorithm):
        self.ambulances = ambulances
        self.cases = cases
        self.ambulance_selection = ambulance_selector

    def run(self):
        raise NotImplementedError()
