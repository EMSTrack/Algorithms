from ems.datasets.location.kd_tree_location_set import KDTreeLocationSet
from ems.generators.location.location import LocationGenerator


class RandomLocationSet(KDTreeLocationSet):

    def __init__(self,
                 count: int,
                 generator: LocationGenerator):
        self.count = count
        self.generator = generator
        latitudes, longitudes = self.generate_locations()
        super().__init__(latitudes, longitudes)

    def generate_locations(self):
        locations = [self.generator.generate() for _ in range(self.count)]
        latitudes = [l.latitude for l in locations]
        longitudes = [l.longitude for l in locations]
        return latitudes, longitudes
