# Runs the simulation.

from typing import List

from ems.algorithms.ambulance_selection import AmbulanceSelectionAlgorithm
from ems.models.ambulance import Ambulance
from ems.models.case import Case


class Simulator:

    def __init__(self,
                 ambulances: List[Ambulance],
                 cases: List[Case],
                 ambulance_selector:  AmbulanceSelectionAlgorithm):

        self.ambulances:List[Ambulance] = ambulances
        self.cases:List[Case] = cases
        self.ambulance_selection:AmbulanceSelectionAlgorithm = ambulance_selector

    def run(self):
        raise NotImplementedError()

    # TODO
    # def coverage(self, ):
