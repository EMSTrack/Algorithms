class Event:

    def __init__(self):
        pass

    def end_time(self):
        raise NotImplementedError


class Dot(Event):
    """ Represents the location of the ambulance over time."""
    def __init__(self, location, starting_time, duration):
        """

        :param location:
        :param starting_time:
        :param duration:
        """
        pass


class Line(Event):
    """ Represents the edge of the ambulance over time. """
    def __duration_as_dots(self):
        """
        Longer distance shown by distance of the line.
        Longer time shown by the number of dots that get drawn before it finishes.
        """

        return None

    def __init__(self, starting_point, ending_point, starting_time, duration):
        """ Defines the points between the starting point and ending point. """
        pass


