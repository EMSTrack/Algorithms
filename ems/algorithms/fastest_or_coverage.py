# Framework for using algorithms and allowing for replacement
from typing import List

from ems.models.ambulance import Ambulance
from ems.models.case import Case
from ems.algorithms.dispatcher_algorithm import BestTravelTimeAlgorithm
from ems.algorithms.calculate_coverage import CoverageAlgorithm

from ems.models.demand import Demand
from ems.algorithms.ambulance_selection import AmbulanceSelectionAlgorithm

# Used by the sim to select ambulances
class FastestAmbulanceBestCoverage(BestTravelTimeAlgorithm, CoverageAlgorithm):
    """
        Barebone class. Users may subclass to implement their own algorithm for
        selecting an ambulance.
    """

    def select_ambulance(self,
                         ambulances: List[Ambulance],
                         case: Case):
        pass
