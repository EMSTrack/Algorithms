from datetime import datetime
from typing import List

from ems.triggers.trigger import Trigger


class TimeframeTrigger(Trigger):

    def __init__(self, start_times: List[datetime],
                 end_times: List[datetime]):
        self.start_times = start_times
        self.end_times = end_times

    def is_active(self,
                  time: datetime):

        for st, et in zip(self.start_times, self.end_times):
            if st <= time <= et:
                return True

        return False
