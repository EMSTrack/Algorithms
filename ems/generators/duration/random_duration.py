# Implementation of an event duration generator that uniformly selects a random duration between two bounds
import random
from datetime import timedelta, datetime

from geopy import Point

from ems.generators.duration.duration import DurationGenerator
from ems.models.ambulances.ambulance import Ambulance


class RandomDurationGenerator(DurationGenerator):

    def __init__(self,
                 lower_bound: float = 5,
                 upper_bound: float = 20):
        self.lower_bound = timedelta(minutes=lower_bound)
        self.upper_bound = timedelta(minutes=upper_bound)

    def generate(self,
                 ambulance: Ambulance = None,
                 destination: Point = None,
                 timestamp: datetime = None):
        seconds_lower_bound = self.lower_bound.total_seconds()
        seconds_upper_bound = self.upper_bound.total_seconds()

        duration_in_seconds = random.randint(seconds_lower_bound, seconds_upper_bound)

        return {'duration': timedelta(seconds=duration_in_seconds)}
