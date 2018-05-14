from geopy import Point


# TODO -- subclass geopy point
class Location:

    def __init__(self,
                 id,
                 point: Point):
        self.id = id
        self.location = point

    def __eq__(self, other):
        """
        Checks for equality
        :return: True if objects are equal; else False
        """

        return type(other) is Location and self.location == other.location
