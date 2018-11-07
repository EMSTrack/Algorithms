from datetime import timedelta

from ems.models.ambulance import Ambulance
from ems.models.cases.case import Case


class CaseRecord:

    def __init__(self,
                 case: Case,
                 ambulance: Ambulance,
                 delay: timedelta,
                 event_history: []):
        self.case = case
        self.ambulance = ambulance
        self.event_history = event_history
        self.delay = delay
