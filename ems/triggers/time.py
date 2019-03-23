from datetime import datetime, timedelta

from ems.triggers.trigger import Trigger


class TimeTrigger(Trigger):

    def __init__(self, start_time: datetime,
                 duration: int,
                 modulus: int = None):
        self.start_time = start_time
        self.duration = timedelta(hours=duration)
        self.modulus = timedelta(hours=modulus) if modulus else None

    def is_active(self,
                  time: datetime):

        if time < self.start_time:
            return False

        diff = time - self.start_time
        if self.modulus:
            diff = diff % self.modulus
            print("diff: {}".format(diff))

        return True if diff < self.duration else False
