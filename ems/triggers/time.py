from datetime import datetime, timedelta

from ems.triggers.trigger import Trigger


class TimeTrigger(Trigger):

    def __init__(self, start_time: datetime,
                 duration: int,
                 modulus: timedelta = None):
        self.start_time = start_time
        self.duration = timedelta(hours=duration)
        self.modulus = modulus

    def is_active(self,
                  time: datetime):

        if time < self.start_time:
            return False

        diff = time - self.start_time
        if self.modulus:
            diff = diff % self.modulus

        return True if diff < self.duration else False
