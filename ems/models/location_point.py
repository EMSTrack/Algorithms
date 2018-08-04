from datetime import datetime

from geopy import Point


class LocationPoint:

    def __init__(self,
                 location: Point = None,
                 timestamp: datetime = None):
        self.location = location
        self.timestamp = timestamp
