# Framework for using algorithms and allowing for replacement
from typing import List

from ems.models.ambulance import Ambulance
from ems.models.case import Case
from ems.algorithms.dispatch_fastest_ambulance import BestTravelTimeAlgorithm
from ems.algorithms.demand_coverage import CoverageAlgorithm

# Used by the sim to select ambulances
class FastestAmbulanceBestCoverage(BestTravelTimeAlgorithm, CoverageAlgorithm):
    """
        Barebone class. Users may subclass to implement their own ambulance_selection for
        selecting an ambulance.
    """

    def select_ambulance(self,
                         ambulances: List[Ambulance],
                         case: Case):
        pass
