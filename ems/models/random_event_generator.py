from ems.models.event import Event


class RandomEventGenerator():

    def __init__(self,
                 timestamp,
                 bounding_box):
        self.timestamp = timestamp
        self.bounding_box = bounding_box

    def generate(self, label):
        return Event(self.timestamp + delta)