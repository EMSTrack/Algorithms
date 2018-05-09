from geopy import Point


class Location:

    def __init__(self, id: int, point: Point):
        self.id = id
        self.location = point
