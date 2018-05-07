from geopy import Point

from ems.models.location import Location


class Demand(Location):

    def __eq__(self, other):
        """
        Checks for equality
        :return: True if objects are equal; else False
        """

        if type(other) is Demand and self.id == other.id:
            return True

        return False
