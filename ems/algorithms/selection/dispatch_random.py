# The following functions define default algorithms for the DispatchAlgorithm class.
import random
from datetime import datetime
from typing import List

from ems.algorithms.selection.ambulance_selection import AmbulanceSelector
from ems.models.ambulances.ambulance import Ambulance
from ems.models.cases.case import Case


# An implementation of a "fastest travel time" ambulance_selection from a base to
# the demand point closest to a case

class RandomSelector(AmbulanceSelector):

    def select_ambulance(self,
                         available_ambulances: List[Ambulance],
                         case: Case,
                         current_time: datetime):

        # Randomly choose
        chosen_ambulance = random.sample(available_ambulances, 1)[0]

        return chosen_ambulance

