# Interface for generating event durations
from datetime import datetime

from geopy import Point

from ems.models.ambulances.ambulance import Ambulance


class EventDurationGenerator:

    def generate(self,
                 ambulance: Ambulance,
                 destination: Point,
                 timestamp: datetime):
        raise NotImplementedError()
