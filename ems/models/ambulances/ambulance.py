from geopy import Point

from ems.models.ambulances.capability import Capability


# Define the Ambulance model.
class Ambulance:

    def __init__(self,
                 identifier: str,
                 base: Point,
                 capability: Capability = Capability.BASIC,
                 deployed: bool = False,
                 location: Point = None):
        self.identifier = identifier
        self.base = base
        self.capability = capability
        self.deployed = deployed
        self.location = location

    def __eq__(self, other):
        """
        Checks for equality
        :return: True if objects are equal; else False
        """

        return type(other) is Ambulance and self.identifier == other.identifier

    def __hash__(self):
        return hash(self.identifier)

    def __str__(self):
        return self.identifier
