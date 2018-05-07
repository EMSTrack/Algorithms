# Runs the simulation.

from typing import List

from ems.algorithms.ambulance_selection import AmbulanceSelectionAlgorithm
from ems.models.ambulance import Ambulance
from ems.models.case import Case


class Simulator:

    def __init__(self,
                 ambulances: List[Ambulance],
                 cases: List[Case],
                 algorithm: AmbulanceSelectionAlgorithm):

        self.ambulances = ambulances
        self.cases = cases
        self.algorithm = algorithm

    def run(self):
        raise NotImplementedError()

    # TODO
    # def coverage(self, ):
