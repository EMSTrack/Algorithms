class Event:

    def __init__(self,
                 timestamp,
                 location,
                 destination,
                 label):
        self.timestamp = timestamp
        self.location = location
        self.destination = destination

        # TODO -- Label should be an enum? e.g. event_type
        self.label = label