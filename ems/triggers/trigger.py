import datetime


class Trigger:

    def is_active(self, time: datetime):
        raise NotImplementedError
