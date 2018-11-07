import datetime
from geopy import Point


class Case:

    # Include events
    def __init__(self,
                 id: int,
                 date_recorded: datetime,
                 incident_location: Point,
                 priority: float = None):
        self.id = id
        self.date_recorded = date_recorded
        self.incident_location = incident_location
        self.priority = priority

    def iterator(self, ambulance, current_time):
        raise NotImplementedError()
