from ems.models.event_type import EventType
from ems.models.location_point import LocationPoint


class Event:

    def __init__(self,
                 origin: LocationPoint,
                 destination: LocationPoint,
                 event_type: EventType):
        self.origin = origin
        self.destination = destination
        self.event_type = event_type
