import datetime
from datetime import datetime
from datetime import timedelta
from geopy import Point

from ems.models.demand import Demand


class Case:

    def __init__(self, id: int, point: Point, dt: datetime,
                 weekday: str, priority: float = None,
                 start_time: datetime = None,
                 finish_time: datetime = None,
                 delay: timedelta = None,
                 closest_demand: Demand = None):


        self.id = id
        self.location = point
        self.weekday = weekday
        self.datetime = dt
        self.priority = priority
        self.start_time = start_time
        self.finish_time = finish_time
        self.delay = delay
        self.closest_demand = closest_demand

    def __eq__(self, other):
        """
        Checks for equality
        :return: True if objects are equal; else False
        """

        if type(other) is Case and self.id == other.id:
            return True

        return False
