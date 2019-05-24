from datetime import datetime, timedelta
from geopy.distance import distance

from geopy import Point

from ems.generators.duration.duration import DurationGenerator
from ems.models.ambulances.ambulance import Ambulance


class DistanceDurationGenerator(DurationGenerator):

    def __init__(self, velocity):
        self.velocity = velocity

    def generate(self,
                 ambulance: Ambulance = None,
                 destination: Point = None,
                 timestamp: datetime = None):
        distance_km = distance(ambulance.location, destination).km
        return timedelta(seconds=int(distance_km/self.velocity))
