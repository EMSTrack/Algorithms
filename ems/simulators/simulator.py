# Runs the simulation.

from typing import List

from ems.algorithms.algorithm import Algorithm
from ems.models.ambulance import Ambulance
from ems.models.case import Case


class Simulator:

    def __init__(self,
                 ambulances: List[Ambulance],
                 cases: List[Case],
                 algorithm: Algorithm):

        self.ambulances = ambulances
        self.cases = cases
        self.algorithm = algorithm

    def run(self):
        raise NotImplementedError()

    # TODO
    # def coverage(self, ):
