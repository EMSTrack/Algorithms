from datetime import datetime, timedelta
import math
import random

from geopy import Point

from ems.generators.duration.duration import DurationGenerator
from ems.models.ambulances.ambulance import Ambulance


# Implementation for a duration generator, where duration until next incident is drawn from the exponential
# distribution with parameter lambda
# lambda = (total # of cases) / (total # of time units in an interval)
# e.g. For 1,000 cases in 40,000 minutes, lambda = 1/40
class PoissonDurationGenerator(DurationGenerator):

    def __init__(self,
                 quantity: int,
                 duration: float):
        self.quantity = quantity
        self.duration = duration
        self.lmda = quantity / duration

    def generate(self,
                 ambulance: Ambulance = None,
                 destination: Point = None,
                 timestamp: datetime = None):
        rand = -math.log(1.0 - random.random())
        minutes_until_next = rand / self.lmda
        return {'duration': timedelta(minutes=minutes_until_next)}
