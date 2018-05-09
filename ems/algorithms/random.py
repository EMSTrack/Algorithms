# The following functions define default algorithms for the DispatchAlgorithm class.
import random
from datetime import datetime
from typing import List

from ems.algorithms.ambulance_selection import AmbulanceSelectionAlgorithm
from ems.models.ambulance import Ambulance
from ems.models.case import Case


# An implementation of a "fastest travel time" ambulance_selection from a base to
# the demand point closest to a case

class RandomAmbulanceSelectionAlgorithm(AmbulanceSelectionAlgorithm):

    def select_ambulance(self,
                         ambulances: List[Ambulance],
                         case: Case,
                         current_time: datetime):

        # Calculate available ambulances
        available = [a for a in ambulances if not a.deployed]

        # Randomly choose
        chosen_ambulance = random.sample(available, 1)

        return {'choice': chosen_ambulance }

