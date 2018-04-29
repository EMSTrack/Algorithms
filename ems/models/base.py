from geopy import Point


class Base:

    def __init__(self, id: int, point: Point):
        self.id = id
        self.location = point
