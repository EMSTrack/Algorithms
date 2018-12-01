# Interface for a "set" of ambulances
class AmbulanceSet:

    def __init__(self, ambulances):
        self.ambulances = ambulances

    def __len__(self):
        raise NotImplementedError()
