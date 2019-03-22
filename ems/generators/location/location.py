# Interface for a location generator
class LocationGenerator:

    def generate(self, timestamp=None):
        raise NotImplementedError()
