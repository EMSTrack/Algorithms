from datetime import datetime, timedelta

from geopy import Point

from ems.algorithms.times.duration_algorithm import DurationAlgorithm
from ems.models.ambulance import Ambulance
from ems.models.case import AbstractCase


class PredeterminedDurationAlgorithm(DurationAlgorithm):
    """
    Implementation of a DurationAlgorithm that returns a constant duration
    """

    def __init__(self, ):
        pass

    def compute_duration(self,
                         ambulance: Ambulance,
                         case: AbstractCase,
                         origin: Point,
                         destination: Point,
                         current_time: datetime):
        pass


