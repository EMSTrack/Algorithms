import pprint
from geopy import Point


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
        self.dots = self.__duration_as_dots()

    def end_time(self):
        return self.ending_time

    def __duration_as_dots(self):
        """ Enumerate over time where the location is"""
        delta = round(self.duration.seconds / 60) + 1
        # if delta < 1: delta = 1

        return [self.location for _ in range(delta)]

    def __str__(self):
        """ For the debuggings """
        return pprint.PrettyPrinter().pformat({
            "location": self.location,
            "starting_time": self.starting_time,
            "duration": self.duration,
            "ending_time": self.ending_time,
            "paths": self.dots  # TODO I know, this is technically a list of the same point.
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
        self.dots = self.__duration_as_dots()

    def __duration_as_dots(self):
        """
        Longer distance shown by distance of the line.
        Longer time shown by the number of dots that get drawn before it finishes.
        """

        # Calculate the delta distance as end-start/minutes
        delta = round(self.duration.seconds / 60) + 1
        # if delta < 1: delta = 1
        dist_lat = self.ending_point.latitude - self.starting_point.latitude
        dist_lon = self.ending_point.longitude - self.starting_point.longitude
        d_lat, d_lon = dist_lat / delta, dist_lon / delta

        # List of [minutes] points between start and end
        return [Point(
            self.starting_point.latitude + time_slice * d_lat,
            self.starting_point.longitude + time_slice * d_lon)
            for time_slice in range(delta)]

    def end_time(self):
        return self.ending_time

    def __str__(self):
        """ For the debuggings """
        return pprint.PrettyPrinter().pformat({
            "starting_point": self.starting_point,
            "ending_point": self.ending_point,
            "starting_time": self.starting_time,
            "duration": self.duration,
            'ending_time': self.ending_time,
            'path': self.dots
        })
