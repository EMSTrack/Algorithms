# Framework for using algorithms and allowing for replacement
from datetime import datetime

from geopy import Point

from ems.models.ambulance import Ambulance

from ems.models.cases.case import Case


# Used by the sim to compute a travel time between one point to another
class DurationAlgorithm:
    """
    Users may subclass to implement their own compute_travel_time for
    computing travel travel_times.
    """

    def compute_duration(self,
                         ambulance: Ambulance,
                         case: Case,
                         origin: Point,
                         destination: Point,
                         current_time: datetime):
        raise NotImplementedError()
