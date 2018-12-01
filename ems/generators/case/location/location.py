# Interface for a location generator
class LocationGenerator:

    def generate(self, timestamp):
        raise NotImplementedError()
