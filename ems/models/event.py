class Event:

    def __init__(self,
                 timestamp,
                 destination,
                 label):
        self.timestamp = timestamp
        self.destination = destination

        # TODO -- Label should be an enum? e.g. event_type
        self.label = label