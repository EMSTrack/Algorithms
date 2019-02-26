# Interface for generating event durations
from datetime   import datetime
from geopy      import Point

from ems.models.ambulances.ambulance import Ambulance


class DurationGenerator:

    # TODO -- use kwargs to support generation of durations w/o ambulance and destination
    def generate(self,
                 ambulance: Ambulance,
                 destination: Point,
                 timestamp: datetime):
        raise NotImplementedError()
