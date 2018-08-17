from typing import List

import datetime.datetime

from geopy import Point

from ems.models.case import AbstractCase
from ems.models.event import Event


class ProcessedCaseData(AbstractCase):

    def __init__(self,
                 id: int,
                 date_recorded: datetime,
                 incident_location: Point,
                 events: List[Event],
                 priority: float = None):
        super().__init__(id, date_recorded, incident_location, priority)
        self.events = events

    def __iter__(self):
        pass


