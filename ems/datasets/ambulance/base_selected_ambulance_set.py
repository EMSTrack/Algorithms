from ems.algorithms.base_selectors.selector import AmbulanceBaseSelector
from ems.datasets.ambulance.ambulance_set import AmbulanceSet
from ems.models.ambulances.ambulance import Ambulance


class BaseSelectedAmbulanceSet(AmbulanceSet):

    def __init__(self,
                 count: int,
                 base_selector: AmbulanceBaseSelector):
        self.count = count
        self.base_selector = base_selector
        super().__init__(self.initialize_ambulances())

    def initialize_ambulances(self):
        bases = self.base_selector.select(self.count)
        ambulances = [Ambulance(identifier=str(i),
                                base=bases[i],
                                location=bases[i]) for i in range(self.count)]

        return ambulances

    def __len__(self):
        return self.count
