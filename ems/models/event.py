from ems.models.event_type import EventType


class Event:

    def __init__(self,
                 timestamp,
                 destination,
                 event_type: EventType):
        self.timestamp = timestamp
        self.destination = destination
        self.event_type = event_type
