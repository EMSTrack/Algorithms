from geopy import Point


class Location:

    def __init__(self, id: int, point: Point):
        self.id = id
        self.location = point

    def __eq__(self, other):
        """
        Checks for equality
        :return: True if objects are equal; else False
        """

        if type(other) is Location and self.id == other.id:
            return True

        return False
