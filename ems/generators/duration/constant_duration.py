from datetime import timedelta, datetime

from geopy import Point

from ems.generators.duration.duration import DurationGenerator
from ems.models.ambulances.ambulance import Ambulance


class ConstantDurationGenerator(DurationGenerator):

    def __init__(self, constant: timedelta):
        self.constant = constant

    def generate(self,
                 ambulance: Ambulance,
                 destination: Point,
                 timestamp: datetime):

        return {'duration': self.constant}