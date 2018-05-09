# Framework for using algorithms and allowing for replacement
from datetime import datetime
from typing import List

from ems.models.ambulance import Ambulance
from ems.models.case import Case


# Used by the sim to select ambulances
class AmbulanceSelectionAlgorithm:
    """
        Barebone class. Users may subclass to implement their own ambulance_selection for
        selecting an ambulance.
    """

    def select_ambulance(self,
                         available_ambulances: List[Ambulance],
                         case: Case,
                         current_time: datetime):
        raise NotImplementedError()
