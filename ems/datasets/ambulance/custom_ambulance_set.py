from ems.algorithms.base_selectors.amb_base_selector import AmbulanceBaseSelector
from ems.datasets.ambulance.ambulance_set import AmbulanceSet
from ems.models.ambulances.ambulance import Ambulance


class CustomAmbulanceSet(AmbulanceSet):

    def __init__(self,
                 ambulance_count: int,
                 base_selector: AmbulanceBaseSelector):
        self.ambulance_count = ambulance_count
        self.base_selector = base_selector
        super().__init__(self.initialize_ambulances())

    def initialize_ambulances(self):
        bases = self.base_selector.select(self.ambulance_count)
        ambulances = [Ambulance(id=str(i),
                                base=bases[i],
                                location=bases[i]) for i in range(self.ambulance_count)]

        return ambulances

    def __len__(self):
        return self.ambulance_count
