from datetime import datetime, timedelta
from random import randrange

from geopy import Point

from ems.algorithms.times.duration_algorithm import DurationAlgorithm
from ems.models.ambulance import Ambulance
from ems.models.cases.case import Case


class RandomDurationAlgorithm(DurationAlgorithm):
    """
    Implementation of a DurationAlgorithm that randomly selects a duration between two bounds
    """

    def __init__(self, lower_bound: timedelta, upper_bound: timedelta):
        self.lower_bound = lower_bound
        self.range = upper_bound - lower_bound

    def compute_duration(self,
                         ambulance: Ambulance,
                         case: Case,
                         origin: Point,
                         destination: Point,
                         current_time: datetime):
        return self.lower_bound + randrange(self.range)
