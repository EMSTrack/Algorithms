# Runs the simulation.

from typing import List

from ems.algorithms.algorithm_set import AlgorithmSet
from ems.models.ambulance import Ambulance
from ems.models.case import AbstractCase


class Simulator:

    def __init__(self,
                 ambulances: List[Ambulance],
                 cases: List[AbstractCase],
                 algorithm_set: AlgorithmSet):
        self.ambulances = ambulances
        self.cases = cases
        self.algorithm_set = algorithm_set

    def run(self):
        raise NotImplementedError()
