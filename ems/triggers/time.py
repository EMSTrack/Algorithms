from datetime import datetime, timedelta

from ems.triggers.trigger import Trigger


# TODO -- Code does not support defining a time trigger with a start time before the start of the sim with some interval
class TimeTrigger(Trigger):

    def __init__(self, start_time: datetime,
                 duration: int,
                 interval: int = None):
        self.start_time = start_time
        self.duration = timedelta(hours=duration)
        self.interval = timedelta(hours=interval) if interval else None

        # Time trigger needs a state
        self.interval_count = 0
        self.was_active = False

    # Returns whether the trigger is active and if so, when the scenario should set the time to
    # TODO -- can outsource the time computation to scenario case set?
    def is_active(self,
                  time: datetime):

        if time < self.start_time:
            return False, None

        diff = time - self.start_time

        if self.interval:
            # diff = diff % self.modulus
            diff = diff - (self.interval * self.interval_count)

        # The trigger has not happened yet
        if diff < timedelta(seconds=0):
            return False, None

        # Two possibilities
        # 1. Scenario has just started and we must rewind back to the start of the time frame
        # 2. Scenario has already been going on and we continue to return True
        #
        # 'Was active' flag helps differentiate
        elif diff <= self.duration:

            # Situation 2
            if self.was_active:
                return True, time

            # Situation 1
            else:
                if self.interval is None:

                    if self.interval_count >= 1:
                        print("this hppnd")
                        return False, None

                    print("not hppnd")

                    return True, self.start_time
                return True, self.start_time + self.interval * self.interval_count

        # Two possibilities
        # 1. Trigger has just ended
        # 2. Given time has jumped too far and skipped this trigger completely; must rewind to start of the
        # time frame
        #
        # Differentiate between situation 1 and 2 with the 'was_active' flag
        elif diff > self.duration:

            # Situation 1
            if self.was_active:
                self.interval_count += 1
                return False, None

            # Situation 2 - Jump back
            else:
                # Must ensure that interval count doesn't repeat on subsequent runs if no interval
                if self.interval is None:

                    if self.interval_count >= 1:
                        print("this hppnd")
                        return False, None

                    print("not hppnd")

                    return True, self.start_time
                return True, self.start_time + self.interval * self.interval_count

        return True, self.start_time if diff <= self.duration else False, None
