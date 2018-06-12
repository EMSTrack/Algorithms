from datetime import datetime
from datetime import timedelta

from geopy import Point

from ems.models.ambulance import Ambulance


class Case:

    def __init__(self,

                 id: int,
                 location: Point,
                 time: datetime,
                 priority: float = None,

                 weekday: str = None,
                 start_time: datetime = None,
                 finish_time: datetime = None,
                 delay: timedelta = None,
                 assigned_ambulance: Ambulance = None):
        self.id = id
        self.location = location
        self.time = time
        self.weekday = weekday
        self.priority = priority
        self.start_time = start_time
        self.finish_time = finish_time
        self.delay = delay
        self.assigned_ambulance = assigned_ambulance

    def start(self, ambulance, start_time, ambulance_travel_time):
        raise NotImplementedError()

    def get_duration(self):
        raise NotImplementedError()

    def get_finish_time(self):
        raise NotImplementedError()

    def __eq__(self, other):
        """
        Checks for equality
        :return: True if objects are equal; else False
        """

        if type(other) is Case and self.id == other.id:
            return True

        return False

    def __str__(self):
        return "\n".join([str(item) for item in [self.id, self.location, self.time, self.weekday, self.priority, self.start_time,
        self.finish_time, self.delay, self.assigned_ambulance]])