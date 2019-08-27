# Interface for a "set" of cases
class CaseSet:

    def __init__(self, time):
        self.time = time

    def iterator(self):
        raise NotImplementedError()

    def get_time(self):
        return self.time

    def set_time(self, time):
        self.time = time
