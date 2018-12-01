# Interface for generating event durations
from datetime import datetime

from geopy import Point

from ems.models.ambulances.ambulance import Ambulance


class EventDurationGenerator:

    def generate(self,
                 ambulance: Ambulance,
                 destination: Point,
                 current_time: datetime):
        raise NotImplementedError()