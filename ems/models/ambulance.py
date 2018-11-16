from geopy import Point


# Define the Ambulance model.

class Ambulance:

    def __init__(self,
                 id: int,
                 base: Point,
                 unit: str = "XXX-XXXX",
                 deployed: bool = False,
                 location: Point = None):
        self.id = id
        self.base = base
        self.unit = unit
        self.deployed = deployed
        self.location = location

    def __eq__(self, other):
        """
        Checks for equality
        :return: True if objects are equal; else False
        """

        if type(other) is Ambulance and self.id == other.id:
            return True

        return False

    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        return str([self.id, self.unit])
