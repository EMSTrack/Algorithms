from datetime import datetime, timedelta

from ems.triggers.trigger import Trigger


# TODO -- Code does not support defining a time trigger with a start time before the start of the sim with some interval
class TimeTrigger(Trigger):

    def __init__(self, start_time: datetime,
                 duration: int,
                 interval: int = None):
        super(TimeTrigger, self).__init__()
        self.start_time = start_time
        self.duration = timedelta(hours=duration)
        self.interval = timedelta(hours=interval) if interval else None

        # Time trigger needs a state
        self.trigger_count = 0

    # Must return a tuple of (boolean, datetime) to represent (has started?, time of start?)
    def has_started(self,
                    time: datetime,
                    **kwargs):

        # Time from start of scenario
        diff = time - self.start_time

        if self.interval:
            diff = diff - (self.trigger_count * self.interval)

        # Time is before the start of the scenario
        if diff < timedelta(seconds=0):
            return False, None

        # If scenario does not repeat and it has already been triggered once
        if self.interval is None:
            if self.trigger_count != 0:
                return False, None
            else:
                return True, self.start_time

        return True, self.start_time + self.interval * self.trigger_count

    # Can assume that this only gets invoked when the scenario is currently active
    # Returns bool for should end
    def has_ended(self,
                  time: datetime,
                  **kwargs):

        diff = time - self.start_time

        if self.interval:
            diff -= self.interval * self.trigger_count

        # Time is before the end of scenario
        if diff < self.duration:
            return False

        # Time is after the end of scenario
        return True

    def mark_ended(self):
        self.trigger_count += 1
