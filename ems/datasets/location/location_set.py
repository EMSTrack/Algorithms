from typing import List

from geopy import Point


class LocationSet:

    def __init__(self, locations: List[Point]):
        self.locations = locations

    def closest(self, point: Point):
        raise NotImplementedError()
