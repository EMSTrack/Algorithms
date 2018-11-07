# Implementation of an event duration generator that uniformly selects a random duration between two bounds
import random
from datetime import timedelta, datetime

from geopy import Point

from ems.models.ambulance import Ambulance


class RandomDurationGenerator:

    def __init__(self,
                 lower_bound: timedelta = timedelta(minutes=5),
                 upper_bound: timedelta = timedelta(minutes=20)):
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    def generate(self,
                 ambulance: Ambulance,
                 destination: Point,
                 current_time: datetime):
        seconds_lower_bound = self.lower_bound.total_seconds()
        seconds_upper_bound = self.upper_bound.total_seconds()

        duration_in_seconds = random.randint(seconds_lower_bound, seconds_upper_bound)

        return timedelta(seconds=duration_in_seconds)