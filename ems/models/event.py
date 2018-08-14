from datetime import timedelta

from geopy import Point

from ems.models.event_type import EventType


class Event:

    def __init__(self,
                 destination: Point,
                 event_type: EventType,
                 duration: timedelta=None):
        self.destination = destination
        self.event_type = event_type
        self.duration = duration
