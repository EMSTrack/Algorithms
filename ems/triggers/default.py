from datetime import datetime

from ems.triggers.trigger import Trigger


class DefaultTrigger(Trigger):

    def is_active(self,
                  time: datetime):
        return True
