import math
import random

from geopy import Point

from ems.generators.location.location import LocationGenerator


# Implementation for a location generator that randomly selects a point uniformly from a circle with given
# center and radius
class CircleLocationGenerator(LocationGenerator):

    def __init__(self,
                 center: Point,
                 radius: float):
        self.center = center
        self.radius = radius

    def generate(self, timestamp):
        direction = random.uniform(0, 2 * math.pi)
        magnitude = self.radius * math.sqrt(random.uniform(0, 1))

        x = magnitude * math.cos(direction)
        y = magnitude * math.sin(direction)

        return Point(latitude=self.center.latitude + y,
                     longitude=self.center.longitude + x)
