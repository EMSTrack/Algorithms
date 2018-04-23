# Runs the simulation.

from typing import List

from ems.algorithms.algorithm import DispatcherAlgorithm
from ems.models.ambulance import Ambulance
from ems.models.base import Base
from ems.models.case import Case
from ems.models.demand import Demand

class Simulator:

    def __init__(self,
                 ambulances: List[Ambulance],
                 bases: List[Base],
                 cases: List[Case],
                 demands: List[Demand],
                 algorithm: DispatcherAlgorithm):

        self.ambulances = ambulances
        self.bases = bases
        self.cases = cases
        self.demands = demands
        self.algorithm = algorithm

    def run(self):
        raise NotImplementedError()

    # TODO
    # def coverage(self, ):
