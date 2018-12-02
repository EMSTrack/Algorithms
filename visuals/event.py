import pprint

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
        self.location = location
        self.starting_time = starting_time
        self.duration = duration
        self.ending_time = starting_time + duration

    def end_time(self):
        return self.ending_time

    def __str__(self):
        return pprint.PrettyPrinter().pformat({
            "location": self.location,
            "starting_time": self.starting_time,
            "duration": self.duration
        })


class Line(Event):
    """ Represents the edge of the ambulance over time. """

    def __init__(self, starting_point, ending_point, starting_time, duration):
        """ Defines the points between the starting point and ending point. """
        self.starting_point = starting_point
        self.ending_point = ending_point
        self.starting_time = starting_time
        self.duration = duration
        self.ending_time = starting_time + duration

    def __duration_as_dots(self):
        """
        Longer distance shown by distance of the line.
        Longer time shown by the number of dots that get drawn before it finishes.
        """

        return None

    def end_time(self):
        return self.ending_time

    def __str__(self):
        return pprint.PrettyPrinter().pformat({
            "starting_point": self.starting_point,
            "ending_point": self.ending_point,
            "starting_time": self.starting_time,
            "duration": self.duration
        })

