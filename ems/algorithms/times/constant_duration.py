from datetime import datetime, timedelta

from geopy import Point

from ems.algorithms.times.duration_algorithm import DurationAlgorithm
from ems.models.ambulance import Ambulance
from ems.models.cases.case import Case


class ConstantDurationAlgorithm(DurationAlgorithm):
    """
    Implementation of a DurationAlgorithm that returns a constant duration
    """

    def __init__(self, constant: timedelta):
        self.constant = constant

    def compute_duration(self,
                         ambulance: Ambulance,
                         case: Case,
                         origin: Point,
                         destination: Point,
                         current_time: datetime):
        return self.constant
