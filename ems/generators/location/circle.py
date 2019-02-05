import math
import random

from geopy import Point

from ems.generators.location.location import LocationGenerator


# Implementation for a location generator that randomly selects a point uniformly from a circle with given
# center and radius (in meters)
class CircleLocationGenerator(LocationGenerator):

    def __init__(self,
                 center_latitude: float,
                 center_longitude: float,
                 radius_km: float):
        self.center = Point(center_latitude, center_longitude)
        self.radius_km = radius_km
        self.radius_degrees = self.convert_radius(radius_km)

    def generate(self, timestamp):
        direction = random.uniform(0, 2 * math.pi)
        magnitude = self.radius_degrees * math.sqrt(random.uniform(0, 1))

        x = magnitude * math.cos(direction)
        y = magnitude * math.sin(direction)

        return Point(latitude=self.center.latitude + y,
                     longitude=self.center.longitude + x)

    def convert_radius(self, radius):
        km_in_one_degree = 110.54
        degrees = radius/km_in_one_degree
        return degrees
