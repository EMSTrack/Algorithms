# The following functions define default algorithms for the DispatchAlgorithm class.
from datetime import timedelta
from typing import List

import geopy
import geopy.distance
import numpy as np

import random

from copy import deepcopy

from scipy.spatial import KDTree

from ems.algorithms.ambulance_selection import AmbulanceSelectionAlgorithm
from ems.data.traveltimes import TravelTimes
from ems.models.ambulance import Ambulance
from ems.models.base import Base
from ems.models.case import Case
from ems.models.demand import Demand


# An implementation of a "fastest travel time" ambulance_selection from a base to
# the demand point closest to a case

class RandomAmbulanceSelectionAlgorithm(AmbulanceSelectionAlgorithm):

    def select_ambulance(self,
                         ambulances: List[Ambulance],
                         case: Case):

        # Calculate available ambulances
        available = [a for a in ambulances if not a.deployed]

        # Randomly choose
        chosen_ambulance = random.sample(available, 1)

        return {'choice': chosen_ambulance }

