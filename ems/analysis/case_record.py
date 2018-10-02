from _ast import List
from datetime import timedelta

from ems.models.ambulance import Ambulance
from ems.models.case import AbstractCase
from ems.models.event import Event


class CaseRecord:

    def __init__(self,
                 case: AbstractCase,
                 ambulance: Ambulance,
                 delay: timedelta,
                 event_history: []):
        self.case = case
        self.ambulance = ambulance
        self.event_history = event_history
        self.delay = delay
