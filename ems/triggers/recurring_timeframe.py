from datetime import datetime, timedelta

from ems.triggers.trigger import Trigger


class RecurringTimeframeTrigger(Trigger):

    def __init__(self, start_time: datetime,
                 duration: timedelta,
                 modulus: timedelta = None):
        self.start_time = start_time
        self.duration = duration
        self.modulus = modulus

    def is_active(self,
                  time: datetime):

        if time < self.start_time:
            return False

        diff = (time - self.start_time) % self.modulus

        return True if diff < self.duration else False
