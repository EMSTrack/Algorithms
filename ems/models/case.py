import datetime

from geopy import Point


class Case:

    def __init__(self, id: int, x: float, y: float, dt: datetime.datetime,
                 weekday: str, priority: float = None,
                 start_time: datetime.datetime = None,
                 finish_time: datetime.datetime = None,
                 delay: datetime.timedelta = None):
        self.id = id
        self.location = Point(x, y)
        self.weekday = weekday
        self.datetime = dt
        self.priority = priority
        self.start_time = start_time
        self.finish_time = finish_time
        self.delay = delay
