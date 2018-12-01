from datetime import timedelta, datetime

from geopy import Point

from ems.generators.event.duration.duration import EventDurationGenerator
from ems.models.ambulances.ambulance import Ambulance


class ConstantDurationGenerator(EventDurationGenerator):

    def __init__(self, constant: timedelta):
        self.constant = constant

    def generate(self,
                 ambulance: Ambulance,
                 destination: Point,
                 timestamp: datetime):
        return self.constant
