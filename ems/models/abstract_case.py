from typing import List


class AbstractCase:

    def __init__(self,
                 id: int,
                 priority: float = None):
        self.id = id
        self.priority = priority

    def iterator(self):
        raise NotImplementedError()

class Event:

    def __init__(self,
                 timestamp,
                 destination,
                 label):
        self.timestamp = timestamp
        self.destination = destination
        self.label = label


class RandomEventGenerator():

    def __init__(self,
                 timestamp,
                 bounding_box):
        self.timestamp = timestamp
        self.bounding_box = bouding_box

    def generate(self, label):
        return Event(self.timestamp + delta)

class RandomCase(AbstractCase):

    def __init__(self,
                 id: int,
                 number_of_events: int,
                 labels: List[str],
                 priority: float = None):
        self.id = id
        self.priority = priority
        self.number_of_events = number_of_events
        self.labels = labels

    def iterator(self):
        k = 0
        events = RandomEventGenerator(timestamp)
        while k < self.number_of_events:
            yield events.generate(self.labels[k])


class ListCase(AbstractCase):

    def __init__(self,
                 id: int,
                 events: List[Event],
                 priority: float = None):
        self.id = id
        self.events = events
        self.priority = priority

    def iterator(self):
        return iter(self.events)

