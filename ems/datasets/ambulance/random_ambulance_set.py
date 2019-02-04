import random

from ems.datasets.ambulance.ambulance_set import AmbulanceSet
from ems.generators.location.location import LocationGenerator
from ems.models.ambulances.ambulance import Ambulance
from ems.models.ambulances.capability import Capability


class RandomAmbulanceSet(AmbulanceSet):

    def __init__(self,
                 count: int,
                 base_generator: LocationGenerator):
        self.count = count
        self.base_generator = base_generator
        super().__init__(self.initialize_ambulances())

    def initialize_ambulances(self):

        ambulances = []
        for index in range(self.count):
            base = self.base_generator.generate(None)
            capability = random.choice(list(Capability))
            ambulances.append(Ambulance(id=str(index),
                                        base=base,
                                        capability=capability,
                                        deployed=False,
                                        location=base))

        return ambulances