from ems.datasets.ambulance.ambulance_set import AmbulanceSet
from ems.datasets.location.location_set import LocationSet
from ems.models.ambulances.ambulance import Ambulance


class CustomAmbulanceSet(AmbulanceSet):

    def __init__(self,
                 bases: LocationSet):
        self.bases = bases
        super().__init__(ambulances=self.initialize_ambulances())

    def initialize_ambulances(self):
        ambulances = [Ambulance(identifier=str(i),
                                base=self.bases[i],
                                location=self.bases[i]) for i in range(len(self.bases))]
        return ambulances

    def __len__(self):
        return len(self.bases)
