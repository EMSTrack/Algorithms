import datetime


class Trigger:

    def __init__(self):
        self.id = None

    def has_started(self, time: datetime, **kwargs):
        raise NotImplementedError

    def has_ended(self, time: datetime, **kwargs):
        raise NotImplementedError

    def set_id(self, identity):
        self.id = identity

    def get_id(self):
        return self.id

    def __eq__(self, other):
        return self.id == other.id
