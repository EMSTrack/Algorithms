import pandas as pd

from ems.algorithms.base_selectors.selector import AmbulanceBaseSelector
from ems.datasets.ambulance.ambulance_set import AmbulanceSet
from ems.models.ambulances.ambulance import Ambulance


class CustomAmbulanceSet(AmbulanceSet):

    def __init__(self,
                 count: int,
                 base_selector: AmbulanceBaseSelector):
        self.count = count
        self.base_selector = base_selector
        super().__init__(self.initialize_ambulances())

    def initialize_ambulances(self):
        bases = self.base_selector.select(self.count)
        ambulances = [Ambulance(id=str(i),
                                base=bases[i],
                                location=bases[i]) for i in range(self.count)]

        return ambulances

    def write_to_file(self, output_filename):
        a = [{"id": ambulance.id,
              "base_latitude": ambulance.base.latitude,
              "base_longitude": ambulance.base.longitude,
              "capability": ambulance.capability.value} for ambulance in self.ambulances]
        df = pd.DataFrame(a, columns=["id", "base_latitude", "base_longitude", "capability"])
        df.to_csv(output_filename, index=False)

    def __len__(self):
        return self.count
