from ems.models.location import Location


class Base(Location):

    def __eq__(self, other):
        """
        Checks for equality
        :return: True if objects are equal; else False
        """

        if type(other) is Base and self.id == other.id:
            return True

        return False
