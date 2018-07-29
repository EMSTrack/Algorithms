from datetime import datetime
from datetime import timedelta
from typing import List

from geopy import Point

from ems.models.ambulance import Ambulance

from ems.models.event import Event
from ems.models.random_event_generator import RandomEventGenerator


# TODO -- Fix up these classes for Event Based Case Implementation
class AbstractCase:

    def __init__(self,
                 id: int,
                 priority: float = None):
        self.id = id
        self.priority = priority

    def iterator(self):
        raise NotImplementedError()


class RandomCase(AbstractCase):

    def __init__(self,
                 id: int,
                 number_of_events: int,
                 labels: List[str],
                 priority: float = None):
        super().__init__(id, priority)
        self.id = id
        self.priority = priority
        self.number_of_events = number_of_events
        self.labels = labels

    def iterator(self):
        k = 0
        events = RandomEventGenerator(timestamp)
        while k < self.number_of_events:
            yield events.generate(self.labels[k])


class ListCase(AbstractCase):

    def __init__(self,
                 id: int,
                 events: List[Event],
                 priority: float = None):
        super().__init__(id, priority)
        self.id = id
        self.events = events
        self.priority = priority

    def iterator(self):
        return iter(self.events)


# TODO -- Remove and replace with Event Based Case Implementation
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