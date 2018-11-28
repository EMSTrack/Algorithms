from typing import List
from datetime import datetime

from ems.models.ambulance import Ambulance
from ems.models.cases.case import Case
from ems.models.events.event import Event


class CaseRecord:

    def __init__(self,
                 case: Case,
                 ambulance: Ambulance,
                 start_time: datetime,
                 event_history: List[Event]):
        self.case = case
        self.ambulance = ambulance
        self.event_history = event_history
        self.start_time = start_time

    def __lt__(self, other):
        return self.case < other.case
