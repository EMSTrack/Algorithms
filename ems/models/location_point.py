from datetime import datetime

from geopy import Point


class LocationPoint:

    def __init__(self,
                 location: Point,
                 timestamp: datetime):
        self.location = location
        self.timestamp = timestamp
