from datetime   import datetime
from typing     import List
from geopy      import Point

from ems.models.cases.case      import Case
from ems.models.events.event    import Event


class DefinedCase(Case):

    def __init__(self,
                 identifier: int,
                 date_recorded: datetime,
                 incident_location: Point,
                 events: List[Event],
                 priority: float = None):

        super().__init__(identifier, date_recorded, incident_location, priority)
        self.events = events

    def iterator(self, ambulance, current_time):
        return iter(self.events)
